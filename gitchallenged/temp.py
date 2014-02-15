 repo.py
 import requests
 import urllib2
 import json

 def repos(lang,diff):
       url = 'https://api.github.com/search/repositories?q=language:' + lang + '&sort=stars&order=desc'
       request = urllib2.Request(url)
       request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
       request.add_header('Content-Type','application/json')
       response = urllib2.urlopen(request)
       json_raw = response.readlines()
       json_object = json.loads(json_raw[0])
       results=[x for x in json_object['items']]
       results=sorted(results,key=lambda x:x['open_issues_count']*x['stargazers_count']*x['watchers_count']*x['forks'])
       return results
