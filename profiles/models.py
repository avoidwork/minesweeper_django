from django.db import models
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    @classmethod
    def register(username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            user = User.objects.create_user(username, password)
            return render_to_response('profiles/ok.html')
        else:
            return render_to_response('profiles/error.html')

    @classmethod
    def login(username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render_to_response('profiles/ok.html')
            else:
                return render_to_response('profiles/disabled.html')
        else:
            return render_to_response('profiles/error.html')