import datetime
import random

import requests


difficulties = [
    'Soft',
    'Medium',
    'Hard',
    'Nightmarishly difficult',
]
difficulties_dict = dict((difficulty, i) for (i, difficulty) in enumerate(difficulties))

def get_repos_scores(lang):
   url = 'https://api.github.com/search/repositories?q=language:%s&per_page=100' % lang
   request = requests.get(url)
   repos = request.json()

   results = list(repos['items'])
   results = sorted(results,key=lambda x:x['open_issues_count']*x['stargazers_count']*x['watchers_count']*x['forks'])
   return results

def get_repos(lang, difficulty, n=10):
    # If the language is python, hardcode in Wikinotes for demo purposes
    repo_score_list = get_repos_scores(lang)
    which_quartile = difficulties_dict[difficulty]
    quartile_size = len(repo_score_list)/4
    start_index = which_quartile * quartile_size
    end_index = (which_quartile + 1) * quartile_size
    desired_repos = repo_score_list[start_index:end_index]
    repos = random.sample(desired_repos, min(len(desired_repos), n))

    if lang == 'Python' and difficulty == 'Easy':
        wikinotes_url = "https://api.github.com/repos/dellsystem/wikinotes"
        response = requests.get(wikinotes_url)
        wikinotes = response.json()
        repos[7] = wikinotes

    return repos


def get_score(issue, current_time=None):
    # Only when calculating the original score
    if current_time is None:
        current_time = datetime.datetime.now()

    text_length = len(issue['body'])
    created_at = datetime.datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ")
    num_seconds_open = (current_time - created_at).total_seconds()
    num_comments = issue['comments']
    return max(int((num_comments + 1) * num_seconds_open * (text_length + 1)/ 10000000), 1)


def get_issues(username, repository, n=10):
    url = 'https://api.github.com/repos/%s/%s/issues?issues=open&per_page=100' % (username, repository)
    request = requests.get(url)
    issues = request.json()
    for issue in issues:
        issue['score'] = get_score(issue)

    return random.sample(issues, min(len(issues), n))
