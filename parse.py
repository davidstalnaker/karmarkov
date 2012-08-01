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
    urls += ['http://reddit.com' + topic['data']['permalink']]
  return urls


def fill_comments_(post, comments):
  if not 'ups' in post:
    return
  karma = post['ups'] - post['downs']
  comments += [(post['body'], karma)]
  if len(post['replies']) == 0:
    return
  for reply in post['replies']['data']['children']:
    fill_comments_(reply['data'], comments)


def get_comments(url):
  """Gets a list of (comment, karma) tuples for a given reddit URL."""
  req = requests.get(url + '.json')
  posts = req.json[1]['data']['children']
  comments = []
  for post in posts:
    fill_comments_(post['data'], comments)
  return comments


def get_comments_from_sub(subreddit, threads=25):
  topics = get_topics(subreddit)[0:threads]
  return reduce (lambda l, c: l + get_comments(c), topics, [])

