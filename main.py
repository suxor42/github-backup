from github import get_organisation_repos
from os import environ

GITHUB_ORGANIZATION = environ['GITHUB_ORGANIZATION']


def clone_repos(repos):
