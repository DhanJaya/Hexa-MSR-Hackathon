import argparse
import json
import datetime
import pytz
from perceval.backends.core.github import GitHub

tz_nz = pytz.timezone('Pacific/Auckland')

parser = argparse.ArgumentParser(
    description="Simple parser for GitHub issues and pull requests"
)
parser.add_argument("-t", "--token", "--nargs", nargs='+', help="GitHub token")
parser.add_argument("-r", "--repo", help="GitHub repository, as 'owner/repo'")

args = parser.parse_args()

(arg1, arg2, arg3, owner, repo) = args.repo.split('/')

repo = GitHub(owner=owner, repository=repo, api_token=args.token)
repo.client = repo._init_client()

f_date = tz_nz.localize(datetime.datetime(2021, 12, 10))
t_date = tz_nz.localize(datetime.datetime(2021, 12, 25))

for item in repo.fetch_items('pull_request', from_date=f_date, to_date=t_date):
    print(item)
    with open('pr-data.json', 'a') as j:
        json.dump(item, j)
