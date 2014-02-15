from django.contrib.auth.models import User


class GithubBackend(object):
    def authenticate(self, username=None):
        return User.objects.get(username=username)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
