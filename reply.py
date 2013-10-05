import facebook
import requests
import sys
import json

if __name__ == '__main__':
  

  oauth_access_token =  'ENTER YOUR ACCES TOKEN HERE'
  graph = facebook.GraphAPI(oauth_access_token)
  profile = graph.get_object("me")
  

  print json.dumps(profile)  