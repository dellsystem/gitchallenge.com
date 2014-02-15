import requests
import simplejson as json


class GithubMeta:

	github_req = requests.get('https://api.github.com/repos/pulls')
	github_json = json.loads(github_req.text)


	def get_repo_list(language):

	def translate_diff():

	def generate_top_n(language, difficulty):

