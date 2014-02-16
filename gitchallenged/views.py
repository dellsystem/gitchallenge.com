import collections
import operator
import json

from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests

from gitchallenged import conf
from gitchallenged.models import Task, UserProfile
from gitchallenged import utils


def home(request):
    if request.user.is_authenticated():
        languages = request.user.get_profile().get_languages()

        context = {
            'difficulties': utils.difficulties,
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
    html_url = user_data['html_url']
    user, created = User.objects.get_or_create(username=username, password='')
    profile = user.get_profile()
    profile.access_token = access_token
    profile.gravatar = gravatar
    profile.repos_url = repos_url
    profile.html_url = html_url
    profile.name = name
    profile.save()

    user = authenticate(username=username)
    login_user(request, user)

    return redirect('home')


def get_repos(request, language, difficulty):
    repos = utils.get_repos(language, difficulty)
    return HttpResponse(json.dumps(repos), content_type='application/json')


def get_issues(request, username, repository):
    issues = utils.get_issues(username, repository)
    return HttpResponse(json.dumps(issues), content_type='application/json')


@login_required
def start(request, username, repository, number):
    access_token = request.user.get_profile().access_token
    if access_token:
        # Fork that shit
        fork_url = 'https://api.github.com/repos/%s/%s/forks%s' % (username, repository, access_token)
        response = requests.post(fork_url)

        # Start the task
        task, created = Task.objects.get_or_create(user=request.user,
            creator_username=username, repository_name=repository,
            number=number)
        context = {
            'task': task,
            'created': created,
        }

        return render(request, 'start.html', context)
    else:
        raise PermissionDenied

@login_required
def your_tasks(request):
    access_token = request.user.get_profile().access_token
    if access_token:
        tasks = Task.objects.filter(user=request.user).order_by('end_time')
        context = {
            'tasks': tasks,
        }

        return render(request, 'your_tasks.html', context)
    else:
        raise PermissionDenied


def scoreboard(request):
    profiles = UserProfile.objects.exclude(access_token='')
    context = {
        'profiles': profiles,
    }
    return render(request, 'scoreboard.html', context)
