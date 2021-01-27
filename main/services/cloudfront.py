import time
from boto.cloudfront import CloudFrontConnection
from boto.cloudfront.distribution import Distribution
from config import settings
import logging
from django.template.context import RequestContext
from django.shortcuts import render_to_response
logger = logging.getLogger('boto')
logger.setLevel(logging.CRITICAL) #disable DEBUG logging that's enabled in AWS by default (outside of django)

# AWS_ACCESS_KEY="AKABCDE1235ABCDEF22A"#SAMPLE
# AWS_SECRET_KEY="a1wd2sD1A/GS8qggkXK1u8kHlh+BiLp0C3nBJ2wW" #SAMPLE
# key_pair_id="APKABCDEF123ABCDEFAG" #SAMPLE
DOWNLOAD_DIST_ID = "E1ABCDEF3ABCDE" #SAMPLE replace with the ID of your Cloudfront dist from Cloudfront console

############################################
def generate_signed_cookies(resource,expire_minutes=5):
    """
    @resource   path to s3 object inside bucket(or a wildcard path,e.g. '/blah/*' or  '*')
    @expire_minutes     how many minutes before we expire these access credentials (within cookie)
    return tuple of domain used in resource URL & dict of name=>value cookies
    """
    if not resource:
        resource = 'images/*'
    dist_id = DOWNLOAD_DIST_ID
    conn = CloudFrontConnection()
    dist = SignedCookiedCloudfrontDistribution(conn,dist_id)
    return dist.create_signed_cookies(resource,expire_minutes=expire_minutes)

############################################
class SignedCookiedCloudfrontDistribution():

    def __init__(self,connection,download_dist_id,cname=True):
        """
        @download_dist_id   id of your Cloudfront download distribution
        @cname          boolean True to use first domain cname, False to use 
                        cloudfront domain name, defaults to cname
                        which presumably matches your writeable cookies ( .mydomain.com)
        """
        self.download_dist = None
        self.domain = None
        try:
            download_dist = connection.get_distribution_info(download_dist_id)
            if cname and download_dist.config.cnames:
                self.domain = download_dist.config.cnames[0] #use first cname if defined
            else:
                self.domain = download_dist.domain_name
            self.download_dist = download_dist
        except Exception, ex:
            logging.error(ex)

    def get_http_resource_url(self,resource=None,secure=False):
        """
        @resource   optional path and/or filename to the resource 
                   (e.g. /mydir/somefile.txt);
                    defaults to wildcard if unset '*'
        @secure     whether to use https or http protocol for Cloudfront URL - update  
                    to match your distribution settings 
        return constructed URL
        """
        if not resource:
            resource = '*'
        protocol = "http" if not secure else "https"
        http_resource = '%s://%s/%s' % (protocol,self.domain,resource)
        return http_resource

    def create_signed_cookies(self,resource,expire_minutes=3):
        """
        generate the Cloudfront download distirbution signed cookies
        @resource   path to the file, path, or wildcard pattern to generate policy for
        @expire_minutes  number of minutes until expiration
        return      tuple with domain used within policy (so it matches 
                    cookie domain), and dict of cloudfront cookies you
                    should set in request header
        """
        http_resource = self.get_http_resource_url(resource,secure=False)    #per-file access #NOTE secure should match security settings of cloudfront distribution
    #    http_resource = self.get_http_resource_url("somedir/*")  #blanket access to all /somedir files inside my bucket
    #    http_resource = self.get_http_resource_url("*")          #blanket access to all files inside my bucket

        #generate no-whitespace json policy, then base64 encode & make url safe
        policy = Distribution._canned_policy(http_resource,SignedCookiedCloudfrontDistribution.get_expires(expire_minutes))
        encoded_policy = Distribution._url_base64_encode(policy)

        #assemble the 3 Cloudfront cookies
        signature = SignedCookiedCloudfrontDistribution.generate_signature(policy,private_key_file=settings.AMAZON_PRIV_KEY_FILE)
        cookies = {
            "CloudFront-Policy" :encoded_policy,
            "CloudFront-Signature" :signature,
            "CloudFront-Key-Pair-Id" :key_pair_id #e.g, APKA..... -> same value you use when you sign URLs with boto distribution.create_signed_url() function
        }
        return self.domain,cookies

    @staticmethod
    def get_expires(minutes):
        unixTime = time.time() + (minutes * 60)
        expires = int(unixTime)  #if not converted to int causes Malformed Policy error and has 2 decimals in value
        return expires

    @staticmethod
    def generate_signature(policy,private_key_file=None):
        """
        @policy     no-whitespace json str (NOT encoded yet)
        @private_key_file   your .pem file with which to sign the policy
        return encoded signature for use in cookie
        """
        #sign the policy - code borrowed from Distribution._create_signing_params()
        signature = Distribution._sign_string(policy, private_key_file)
        #now base64 encode the signature & make URL safe
        encoded_signature = Distribution._url_base64_encode(signature)
        return encoded_signature

############################################
def sample_django_view_method(request,template="mytemplate.html"):
    expireLen = 30 #30 minutes
    s3resource = "somepath_in_my_bucket/afile.mp4"
    context = {} #variables I'm passing to my html template
    response = render_to_response(template, context, context_instance=RequestContext(request))
    domain,cookies = generate_signed_cookies(s3resource,expire_minutes=expireLen)
    #TROUBLESHOOTING COOKIES:
    #NOTE - Cookie Domain must be a domain you control that spans your app & your Cloudfront CNAME
    #NOTE - (e.g. if my webapp is www.mydomain.com and my AWS Download Distribution has cname cloud.mydomain.com, cant set cookies from webapp to 
            # www.mydomain.com or localhost.mydomain.com or cloud.mydomain.com and have them work 
        # -> instead set cookies to .mydomain.com to work across sub-domains, you can then verify in request headers to CloudFront that these cookies get passed.
        # TIP - if you set_cookies from a page with a .mydomain.com suffix, but don't see them get set in Chrome they didn't get set because of permissions - can't set to a diff subdomain or diff base domain
        # TIP - if you set_cookies and see them in Chrome but don't see them in request headers to Cloudfront, cookie domain is likely too narrow, need to widen to span subdomains
    base_domain = '.mydomain.com'
    # NOTE: Sanity check when testing so you can flag any gotchas - I have not fully tested using non-cname urls inside policy vs all possible domains for cookie itself   
    if not domain.endswith(base_domain):
        logger.warn("This likely won't work - your resource permissions use a different domain than your cookies")
    for name,value in cookies.items():
        response.set_cookie(name,value=value,httponly=True,domain=base_domain)
    return response

############################################