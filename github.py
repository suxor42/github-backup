from github3 import login
from os import environ

GITHUB_USER = environ['GITHUB_USER']
GITHUB_PASSWORD = environ.get('GITHUB_PASSWORD')
GITHUB_TOKEN = environ.get('GITHUB_TOKEN')

if GITHUB_TOKEN is None and GITHUB_PASSWORD is None:
  raise ValueError('GITHUB_TOKEN or GITHUB_PASSWORD have to be set')

ghclient = login(username=GITHUB_USER, password=GITHUB_PASSWORD, token=GITHUB_TOKEN)


def get_organisation_repos(organisation):
  organisation = filter(lambda org: org.login == organisation, ghclient.iter_orgs()).__next__()
  repositories = list(organisation.iter_repos())
  repositories = map(lambda repo: repo.git_url, repositories)
  return list(repositories)


if __name__ == '__main__':
  get_organisation_repos('upday')