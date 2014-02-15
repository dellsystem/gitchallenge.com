import collections
import operator

from django.contrib.auth.models import User
from django.db import models
import requests

from gitchallenged import conf


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=40)
    gravatar = models.CharField(max_length=48)
    name = models.CharField(max_length=100)
    repos_url = models.URLField()

    def get_client_string(self):
        return 'client_id=%s&client_secret=%s' % (conf.CLIENT_ID, conf.CLIENT_SECRET)

    def get_languages(self):
        client_string = self.get_client_string()
        repos_url = self.repos_url + self.access_token + client_string
        repos_response = requests.get(repos_url)
        repos = repos_response.json()
        language_counts = collections.defaultdict(int)

        for repo in repos:
            # Make a request to get the languages for that repository
            languages_url = '%s?%s' % (repo['languages_url'], client_string)
            languages_response = requests.get(languages_url)
            languages = languages_response.json()

            for language, count in languages.iteritems():
                language_counts[language] += count

        languages = sorted(language_counts.items(), key=operator.itemgetter(1),
            reverse=True)

        return languages


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# Register a handler for the post_save signal to ensure every user has a profile
models.signals.post_save.connect(create_user_profile, sender=User)
