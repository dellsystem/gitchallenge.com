from django.core.exceptions import PermissionDenied
from django.shortcuts import render
import requests

from gitchallenged import conf
from gitchallenged.models import UserProfile


def home(request):
    context = {
        'client_id': conf.CLIENT_ID,
    }

    return render(request, 'home.html', context)


def login(request):
    return render(request, 'home.html')


def authorise(request):
    print "getting code"
    code = request.POST.get('code')
    if not code:
        raise PermissionDenied

    print "About to post to login"

    # Otherwise, use this code to get an access token from GitHub using OAuth
    login_url = 'https://github.com/login/oauth/access_token'
    login_response = requests.post(login_url, data={
        'client_id': conf.CLIENT_ID,
        'client_secret': conf.CLIENT_SECRET,
        'code': code,
        'redirect_uri': 'http://gitchallenged.com/dashboard/',
    })
    login_response_data = login_response.json()
    access_token = login_response_data.get('access_token')
    print access_token
    scopes = login_response_data.get('scopes')
    print scopes

    # Get some basic data about this user (username, first name, last name)
    # Eventually needs to check that the token is still valid each time
    user_url = 'https://api.github.com/user'
    user_response = requests.get(user_url, data={
        'access_token': access_token,
    })
    user_response_data = user_response.json()
    print user_response_data

    # Create a user for this person (if one doesn't exist already)
    #user = User.objects.get_or_create(username=
    # Add the access token to the user's profile

    return render(request, 'home.html')
