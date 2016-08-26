from github import get_organisation_repos
from os import environ, stat, mkdir, remove
from shutil import rmtree
from subprocess import call
from datetime import datetime
import re
import boto3

GITHUB_ORGANIZATION = environ['GITHUB_ORGANIZATION']
S3_BUCKET = environ['S3_BUCKET']


def clone_repo(dir, repo):
  reponame_pattern = re.compile('.*/(?P<repo_name>.*)\.git$')
  repo_name = reponame_pattern.match(repo).group('repo_name')
  print(repo)
  call("bash -c \"cd {dir}; git clone {repo}\"".format(dir=dir, repo=repo), shell=True)


def archive(dir, postfix):
  call("bash -c \"tar -czf {dir}-{postfix}.tar.gz {dir}\"".format(dir=dir, postfix=postfix), shell=True)
  return "{dir}-{postfix}.tar.gz".format(dir=dir, postfix=postfix)

def upload_to_s3(bucket, prefix, file):
  s3 = boto3.resource('s3')
  if bucket not in map(lambda bucket: bucket.name, s3.buckets.all()):
    s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
  s3.Object(bucket, "%s/%s" % (prefix, file)).put(Body=open(file, 'rb'))




if __name__ == '__main__':
  dir = 'backup'
  time = datetime.today()
  try:
    stat(dir)
  except:
    mkdir(dir)

  for repo in get_organisation_repos(GITHUB_ORGANIZATION):
    clone_repo(dir, repo)
  file_name = archive(dir, time.strftime('%Y-%m-%d-%H-%M-%S'))
  upload_to_s3(S3_BUCKET, time.strftime('%Y/%m/%d'), file_name)
  rmtree(dir, ignore_errors=True)
  remove(file_name)

