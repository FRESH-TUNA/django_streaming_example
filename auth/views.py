from django.contrib import auth
from django.contrib.auth import authenticate
from .models import User
from django.http import HttpResponse
import json
from django.shortcuts import render, redirect
import logging

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
        return redirect('main:videos-list')
    else:
        return render(request, "auth/login.html")

def logout(request):
    auth.logout(request)
    return redirect('main:videos-list')
