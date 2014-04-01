from profiles.models import UserProfile
from django.shortcuts import render, render_to_response

def login(request):
    return render_to_response('profiles/login.html')

def register(request):
    return render_to_response('profiles/register.html')