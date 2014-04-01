from django.http import HttpResponse
from profiles.models import UserProfile
from django.shortcuts import render, render_to_response
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "HEAD", "OPTIONS", "POST"])
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        UserProfile.register(username, password)
    return render_to_response('profiles/login.html')

@require_http_methods(["GET", "HEAD", "OPTIONS", "POST"])
def register(request):
    return render_to_response('profiles/register.html')