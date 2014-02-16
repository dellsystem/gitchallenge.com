import random

import requests


difficulties = {
	"Easy": 0,
	"Medium": 1,
	"Hard":	2,
	"I want to crush my ego": 3,
}

def get_repos_scores(lang):
   url = 'https://api.github.com/search/repositories?q=language:%s&per_page=100' % lang
   request = requests.get(url)
   repos = request.json()

   results = list(repos['items'])
   results = sorted(results,key=lambda x:x['open_issues_count']*x['stargazers_count']*x['watchers_count']*x['forks'])
   return results

def get_repos(lang, difficulty, n=10):
	repo_score_list = get_repos_scores(lang)
	which_quartile = difficulties[difficulty]
	quartile_size = len(repo_score_list)/4
	start_index = which_quartile * quartile_size
	end_index = (which_quartile + 1) * quartile_size
	desired_repos = repo_score_list[start_index:end_index]
	return random.sample(desired_repos, min(len(desired_repos), n))
