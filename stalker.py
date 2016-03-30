#!/usr/bin/env python2
'''
  @Author: Josh Snider
'''
import argparse
import getpass
from github import Github
import json
import os
import re
import subprocess
import sys

def get_repos(gh_agent):
  ''' Get the repos to clone.'''
  user = gh_agent.get_user().login
  for repo in gh_agent.get_user().get_repos():
    if repo.full_name.startswith(user):
      yield repo
  for org in gh_agent.get_user().get_orgs():
    for repo in org.get_repos():
      yield repo

def make_args():
  ''' Make the parser for the command line.'''
  parser = argparse.ArgumentParser(
    description="Clone all of your GitHub repos. Including private repos.")
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--user', help="Your github username")
  group.add_argument('--token',
    help="OAuth token. Alternative to password authentication.")
  group = parser.add_mutually_exclusive_group()
  return parser

def make_github_agent(cli_args):
  ''' Create the Github object used
      to access their API.'''
  gh_agent = None
  if cli_args.token:
    gh_agent = Github(cli_args.token)
  else:
    user = cli_args.user
    if not user:
      print 'User:',
      user = sys.stdin.readline().strip()
    passw = getpass.getpass('Password:')
    gh_agent = Github(user, passw)
  return gh_agent

def main():
  ''' Sync a user's GitHub repos with the current machine.'''
  parser = make_args()
  args = parser.parse_args()
  gh_agent = make_github_agent(args)
  os.mkdir('stalker')
  os.chdir('stalker')
  for repo in get_repos(gh_agent):
    print(repo.full_name)
    subprocess.call(["git", "clone",
                   "https://github.com/" + repo.full_name])

if __name__ == '__main__':
  main()
