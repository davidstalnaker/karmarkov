#!/usr/bin/python

import json
import requests


def get_topics(subreddit, prev=None):
  """Gets the URLS of the top topics from the given subreddit in the last year."""
  if prev:
    prev_text = '&after=%s' % prev
  else:
    prev_text = ''
  url = 'http://reddit.com/r/%s/top.json?sort=top&t=year%s' % (subreddit, prev_text)
  print(url)
  req = requests.get(url, headers={'User-Agent': 'karmarkov-bot'})
  if req.status_code != 200:
    print "HTTP error :("
    return []
  urls = []
  for topic in req.json['data']['children']:
    urls += ['http://reddit.com' + topic['data']['permalink']]
  last_topic = req.json['data']['children'][-1]['data']['name']
  return urls, last_topic


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
  print(url)
  req = requests.get(url + '.json', headers={'User-Agent': 'karmarkov-bot'})
  posts = req.json[1]['data']['children']
  comments = []
  for post in posts:
    fill_comments_(post['data'], comments)
  return comments


def get_comments_from_sub(subreddit, threads=25):
  topics = set()
  last_topic = None
  for i in range(0, threads, 25):
    new_topics, last_topic = get_topics(subreddit, prev=last_topic)
    if i + 25 > threads:
      topics.update(new_topics[:threads % 25])
    else:
      topics.update(new_topics)
  return reduce (lambda l, c: l + get_comments(c), topics, [])

