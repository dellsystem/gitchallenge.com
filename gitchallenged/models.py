import collections
import datetime
import operator

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
import requests

from gitchallenged import conf
from gitchallenged import utils


class Task(models.Model):
    user = models.ForeignKey(User)
    creator_username = models.CharField(max_length=255)
    repository_name = models.CharField(max_length=255)
    number = models.IntegerField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    points_gained = models.IntegerField(default=0)

    def __unicode__(self):
        return "issue #%s for %s/%s" % (self.number, self.creator_username,
            self.repository_name)

    def finish(self, should_get_points=False):
        issue_url = 'https://api.github.com/repos/%s/%s/issues/%s' % (
            self.creator_username, self.repository_name, self.number)
        issue = requests.get(issue_url).json()

        # Only gain points if the user submitted a pull request
        self.points_gained = utils.get_score(issue,
            current_time=self.start_time.replace(tzinfo=None))
        self.end_time = datetime.datetime.now()
        self.save()

    def get_absolute_url(self):
        return reverse('start', args=[self.creator_username,
            self.repository_name, self.number])


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=40)
    gravatar = models.CharField(max_length=48)
    name = models.CharField(max_length=100)
    repos_url = models.URLField()
    html_url = models.URLField()
    total_score = models.IntegerField()

    def get_client_string(self):
        return 'client_id=%s&client_secret=%s' % (conf.CLIENT_ID, conf.CLIENT_SECRET)

    def get_languages(self):
        client_string = self.get_client_string()
        repos_url = self.repos_url + self.access_token + client_string
        repos_response = requests.get(repos_url)
        repos = repos_response.json()
        language_counts = collections.Counter()

        for repo in repos:
            language = repo['language']
            if language:
                language_counts[language] += 1

        languages = sorted(language_counts.items(), key=operator.itemgetter(1),
            reverse=True)

        return languages



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# Register a handler for the post_save signal to ensure every user has a profile
models.signals.post_save.connect(create_user_profile, sender=User)
