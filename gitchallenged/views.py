import collections
import operator
import json

from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests

from gitchallenged import conf
from gitchallenged.models import UserProfile


def home(request):
    # Figure out the languages by doing a bunch of API requests
    profile = request.user.get_profile()
    repos_url = profile.repos_url + profile.access_token
    repos_response = requests.get(repos_url)
    repos = repos_response.json()
    language_counts = collections.defaultdict(int)

    for repo in repos:
        # Make a request to get the languages for that repository
        languages_url = repo['languages_url']
        languages_response = requests.get(languages_url)
        languages = languages_response.json()

        for language, count in languages.iteritems():
            language_counts[language] += count

    languages = sorted(language_counts.items(), key=operator.itemgetter(1),
        reverse=True)

    difficulties = [
        'Easy',
        'Medium',
        'Hard',
        'Fuck you guys',
    ]

    if request.user.is_authenticated():
        context = {
            'difficulties': difficulties,
            'profile': request.user.get_profile(),
            'languages': languages,
        }
        return render(request, 'dashboard.html', context)
    else:
        context = {
            'client_id': conf.CLIENT_ID,
        }

        return render(request, 'home.html', context)


def logout(request):
    logout_user(request)
    return redirect('home')


def login(request):
    return redirect('home')


def authorise(request):
    code = request.GET.get('code')
    if not code:
        raise PermissionDenied

    # Otherwise, use this code to get an access token from GitHub using OAuth
    login_url = 'https://github.com/login/oauth/access_token'
    login_response = requests.post(login_url, data={
        'client_id': conf.CLIENT_ID,
        'client_secret': conf.CLIENT_SECRET,
        'code': code,
    })
    access_token = '?' + login_response.text

    # Get some basic data about this user (username, first name, last name)
    # Eventually needs to check that the token is still valid each time
    user_url = 'https://api.github.com/user' + access_token
    user_response = requests.get(user_url)
    user_data = user_response.json()

    # Create a user for this person (if one doesn't exist already) and add the
    # the access token to the user's profile
    username = user_data['login']
    gravatar = user_data['gravatar_id']
    name = user_data['name']
    repos_url = user_data['repos_url']
    user, created = User.objects.get_or_create(username=username, password='')
    profile = user.get_profile()
    profile.access_token = access_token
    profile.gravatar = gravatar
    profile.repos_url = repos_url
    profile.name = name
    profile.save()

    user = authenticate(username=username)
    login_user(request, user)

    return redirect('home')


def get_repos(request, language, difficulty):
    repo = {
        'title': 'Wikinotes',
        'description': 'A free and open source resource for courses etc',
        'author': 'dellsystem',
        'num_stars': 31,
        'avatar_url': 'https://gravatar.com/avatar/13ff8dc8c2bf2a4752816e1e3f201a05?d=https%3A%2F%2Fidenticons.github.com%2F76dc611d6ebaafc66cc0879c71b5db5c.png&r=x',
    }
    data = [repo] * 5
    return HttpResponse(json.dumps(data), content_type='application/json')
