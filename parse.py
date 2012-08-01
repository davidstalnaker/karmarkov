#!/usr/bin/python

import json
import requests


def get_topics(subreddit):
  """Gets the URLS of the top topics from the given subreddit in the last year."""
  url = 'http://reddit.com/r/%s/top.json?sort=top&t=year' % subreddit
  req = requests.get(url)
  if req.status_code != 200:
    print "HTTP error :("
    return []
  urls = []
  for topic in req.json['data']['children']:
    urls += [topic['data']['url']]
  return urls




