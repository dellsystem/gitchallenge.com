from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=40)
    gravatar = models.CharField(max_length=48)
    name = models.CharField(max_length=100)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# Register a handler for the post_save signal to ensure every user has a profile
models.signals.post_save.connect(create_user_profile, sender=User)
