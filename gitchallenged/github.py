import random

import requests
import simplejson as json


difficulties = {
	"easy": 0,
	"medium": 1,
	"hard":	2,
	"You gotta be fuckin' kiddin": 3				
}

def get_repos_scores(lang, diff):
   url = 'https://api.github.com/search/repositories?q=python+language:' + lang + '&sort=stars&order=desc'
   github_language_request = requests.get(url)
   github_language_request_json = json.loads(github_language_request)

   results=list(github_language_request_json['items'])
   results=sorted(results,key=lambda x:x['open_issues_count']*x['stargazers_count']*x['watchers_count']*x['forks'])
   return results

def get_repos(lang, diff, n=10):
	repo_score_list = get_repos_scores(lang, diff)
	which_quartile = difficulties[diff]
	quartile_size = len(repo_score_list)/4
	start_index = which_quartile * quartile_size 
	end_index = (which_quartile + 1) * quartile_size
	desired_repos = repo_score_list[start_index:end_index]
	return random.sample(desired_repos, n)

class GithubUser(username):
	def is_empty(any_structure):
	    if any_structure:
	        print('Structure is not empty.')
	        return False
	    else:
	        print('Structure is empty.')
	        return True

	url = 'https://api.github.com/users/' + username
	githubUserRequest = requests.get(url)
	githubUserJson = json.loads(githubUserRequest.text)

	def getAvatarURL():
		return githubUserJson['avatar_url']
	def getUserFullName():
		return githubUserJson['name']
	def getUserEmail():
		return githubUserJson['email']
	
	githubUserRepoRequest = requests.get(url + "repos")	
	githubUserRepoJson = json.loads(githubUserRequest.text)

	def getTopLanguages():
		topLanguageURLs = []
		for repo in githubUserRepoJson:
			getTopLanguages.append(repo["languages_url"])



