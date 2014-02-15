import requests
import simplejson as json
from pprint import pprint
githubReq = requests.get('https://api.github.com/repos/dellsystem/wikinotes/pulls')
githubJson = json.loads(githubReq.text)
for shit in githubJson:
	print 'Title: ' + shit["title"]
	print 'State: ' + shit["state"]
	if shit["created_at"] and shit["merged_at"] != None:
		print 'Created at: ' + shit["created_at"]
		print 'Merged at: ' + shit["merged_at"]
	elif shit["created_at"] is None:
		print 'Created at: null'
	elif shit["merged_at"] is None:
		print 'Created at: null'
	print "---------"


class GithubRepo(reponame, )

class GithubIssue()

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


class GithubMeta()