import operator

import requests


def check_score(request):
    user = request.user
    completed_issues = []
    lost_issues = []

    if user.is_authenticated():
        profile = user.get_profile()
        if profile.access_token:
            # Go through all the tasks
            for task in user.task_set.filter(end_time__isnull=True):
                # First check if the task is closed
                issue_url = 'https://api.github.com/repos/%s/%s/issues/%s' % (
                    task.creator_username, task.repository_name, task.number)
                issue = requests.get(issue_url).json()

                # Make sure this user submitted a merged pull req
                if issue['closed_at'] is not None:
                    pulls_url = 'https://api.github.com/repos/%s/%s/pulls%s&state=closed' % (
                        task.creator_username, task.repository_name,
                        profile.access_token)
                    pulls_response = requests.get(pulls_url)
                    pulls = pulls_response.json()

                    # If the issue is closed, and the author has a merged pull request referencing the issue in one of the commits, they win points
                    for pull in pulls:
                        if pull['user']['login'] == user.username:
                            # Done!
                            task.finish(should_get_points=True)
                            completed_issues.append(task)
                            break

                    # Otherwise, it was closed by someone else.
                    if task.end_time is None:
                        task.finish(should_get_points=False)
                        lost_issues.append(task)


    show_modal = lost_issues or completed_issues

    context = {
        'lost_issues': lost_issues,
        'completed_issues': completed_issues,
        'show_modal': show_modal,
    }

    return context
