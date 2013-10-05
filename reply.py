#!/usr/bin/env python
"""reply.py: Replies to Birthday wishes on your Facebook wall"""
__author__ = "Keith Mascarenhas"
__copyright__ = "Copyright 2013, Keith Mascarenhas"
__credits__ = ["Akshit Khurana at Quora.com for the idea: http://www.quora.com/Python-programming-language-1/What-are-the-best-Python-scripts-youve-ever-written"]
__email__ = "keithxm23@gmail.com"

import facebook # pip install facebook-sdk
import requests # pip install requests
import datetime
# #TODO from dateutil.parser import parse # pip install python-dateutil
from calendar import timegm
from utils import already_replied, pretty_date

if __name__ == '__main__':
  
  #bday = '22/10/2013' # For good measure, enter a day before your actual birthdate this year in DD/MM/YYYY
  bday = '24/08/2013'
  unix_bday = str(timegm(datetime.datetime.strptime(bday, "%d/%m/%Y").utctimetuple()))

  oauth_access_token =  ''
  graph = facebook.GraphAPI(oauth_access_token)
  profile = graph.get_object("me")
  post_ids = graph.fql("SELECT post_id FROM stream WHERE source_id = me() AND created_time > " +unix_bday+ " LIMIT 500")
  posts = graph.get_objects([x['post_id'] for x in post_ids])
  
  
  #TODO First filter out posts by self either by filter() or using filter_key in fql
  ordered_posts = sorted(posts.items(), key = lambda x :x[1]['created_time'], reverse=True)
  replies = [] # List that will hold replies in tuples as (<post_id>, <message>)
  for p in dict(ordered_posts):
    if profile['name'] != posts[p]['from']['name'] and not already_replied(profile['name'], posts[p]):
      if 'message' not in posts[p].keys():
        print posts[p]['from']['name'] +" posted a message on your wall with no text. Maybe it's a pic/video/link. You should probably have a look at this message and reply manually"
        continue
      print posts[p]['from']['name'] +' wrote on your wall: '# #TODO at '+pretty_date(parse(posts[p]['created_time']))+' :'

      print "\t"+posts[p]['message']
      reply = raw_input('Type your reply and hit enter: ')
      replies.append((p,reply,posts[p]['from']['name']))
  
  for r in replies:
    if r[1] != '':
      graph.put_comment(r[0], message=r[1])
      print 'Replied to '+r[2]+' with: "'+r[1]+'"'
      
  print 'Completed sending out all replies!'