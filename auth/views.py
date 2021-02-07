from django.contrib import auth
from django.contrib.auth import authenticate
from .models import User
from django.http import HttpResponse
from .services.cloudfront import CloudFrontUtil
from django.conf import settings
from django.shortcuts import render, redirect
import datetime
import os

def signup(request):
    if request.method == "POST":
        user = User.objects.create_user(
            email=request.POST.get('username'), 
            password=request.POST.get('password')
        )
        if user is not None:
            auth.login(request, user)
        return redirect('main:videos-list')
    else:
        return render(request, "auth/signup.html")

def login(request):
    if request.method == "POST":
        user = authenticate(
            email=request.POST.get('username'), 
            password=request.POST.get('password')
        )
        if user is not None:
            auth.login(request, user)
            cloudfrontutil = CloudFrontUtil(settings.CLOUDFRONT_PRIVATE_KEY, settings.CLOUDFRONT_KEY_PAIR_ID)
            response = redirect('main:videos-list')
            if os.environ['DJANGO_SETTINGS_MODULE'] == 'config.settings.production':
                signed_cookies = cloudfrontutil.generate_signed_cookies(
                    f"https://{settings.CLOUDFRONT_URL}/*", datetime.datetime.now() + datetime.timedelta(days=1))
                for name,value in signed_cookies.items():
                    response.set_cookie(
                        name,value=value,httponly=True,domain=settings.ALLOWED_HOST[0])
            return response
        return redirect('main:videos-list')
    else:
        return render(request, "auth/login.html")

def logout(request):
    auth.logout(request)
    return redirect('main:videos-list')

