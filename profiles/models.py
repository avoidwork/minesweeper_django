from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def register(username, password):
        user = User.objects.create_user(username, password)
        return user