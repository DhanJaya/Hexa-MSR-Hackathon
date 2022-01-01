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


def run_graal_analysis(url, start_date, end_date):

    repo_owner = help.extract_owner_repo_name_from_url(url)
    owner = repo_owner['owner']
    repo = repo_owner['repo']
    directory = '/tmp/' + repo
    # Remove directories in case they already exist
    remove_directories(directory)
    # 2017-01-18T07:01:56Z  2019-10-05T02:35:16Z
    from_date = datetime.datetime(2019, 9, 21, 00, 00, 00,
                                  tzinfo=dateutil.tz.tzutc())
    # 2017-04-28T18:20:56Z
    to_date = datetime.datetime(2019, 10, 8, 00, 00, 00,
                                tzinfo=dateutil.tz.tzutc())

    repo_uri = 'https://github.com/' + owner + '/' + repo
    cocom = CoCom(uri=repo_uri, git_path=directory)
    print('Scanning repositories.....')
    items = cocom.fetch(from_date=from_date, to_date=to_date)

    file1 = open("myfile3.txt", "a")

    for commit in items:
        print(commit['data']['commit'] + ", ")
        print(commit['search_fields']['item_id'] + ", ")
        print(commit['data']['AuthorDate'] + ", ")
        print(commit['data']['analysis'])
        print('_________________________________________________________________________________')
    #  file1.write(commit['data']['commit'] + ", ")
    # file1.write(commit['data']['AuthorDate'] + ", ")
    # file1.write(json.dumps(commit['data']['analysis']))
    # file1.write('\n')
    # with open('vulns.json', 'a') as j:
    #     json.dump(commit, j)
    file1.close()
    remove_directories()
