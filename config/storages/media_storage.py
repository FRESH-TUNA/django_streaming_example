from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    # location = 'media'
    file_overwrite = False
    # def read_manifest(self):
    #     try:
    #         return super(ManifestStaticFilesStorage,self).read_manifest()
    #     except IOError:
    #         return None
    