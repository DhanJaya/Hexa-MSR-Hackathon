import json
import os
import shutil
import datetime
import dateutil.tz

from graal.backends.core.cocom import CoCom
import util.helper as help


def remove_directories(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print('Removed: '+directory)
    if os.path.exists('/tmp/worktrees'):
        shutil.rmtree('/tmp/worktrees')
        print('Removed: /tmp/worktrees')


def run_graal_analysis(url, start_date, end_date, commits):

    repo_owner = help.extract_owner_repo_name_from_url(url)
    owner = repo_owner['owner']
    repo = repo_owner['repo']
    directory = '/tmp/' + repo

    # Remove directories in case they already exist
    remove_directories(directory)
    # 2017-01-18T07:01:56Z  2019-10-05T02:35:16Z
    from_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
    days = datetime.timedelta(1)
    new_from_date = from_date - days
    # 2017-04-28T18:20:56Z
    to_date = datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ")
    to_date += datetime.timedelta(days=1)
    repo_uri = 'https://github.com/' + owner + '/' + repo
    cocom = CoCom(uri=repo_uri, git_path=directory)
    print('Scanning repositories.....')
    items = cocom.fetch(from_date=new_from_date, to_date=to_date)

    commit_analysis = {}
    try:
        for commit in items:
            if commit['data']['commit'] in commits:
                print(commit['data']['commit'] + ", ")
                print(commit['search_fields']['item_id'] + ", ")
                print(commit['data']['AuthorDate'] + ", ")
                print(commit['data']['analysis'])
                print('_________________________________________________________________________________')
                commit_analysis[commit['data']['commit']] = json.dumps(commit['data']['analysis'])
    except Exception as exe:
        print('Error occurred in {} : {}'.format(url, exe))

    remove_directories(directory)
    return commit_analysis
