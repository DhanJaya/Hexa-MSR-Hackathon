import json
import os
import shutil
import datetime
import dateutil.tz

import json

from graal.backends.core.cocom import CoCom

#https://github.com/apache/tomcat
#https://github.com/alibaba/fastjson
#https://github.com/apache/ambari
owner = 'apache'
repo = 'tomcat'
directory = '/tmp/' + repo


def remove_directories():
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print('Removed: '+directory)
    if os.path.exists('/tmp/worktrees'):
        shutil.rmtree('/tmp/worktrees')
        print('Removed: /tmp/worktrees')


# Remove directories in case they already exist
remove_directories()
#2017-01-18T07:01:56Z
from_date = datetime.datetime(2017, 1, 17, 00, 00, 00,
                              tzinfo=dateutil.tz.tzutc())
#2017-04-28T18:20:56Z
to_date = datetime.datetime(2017, 4, 29, 00, 00, 00,
                                     tzinfo=dateutil.tz.tzutc())

repo_uri = 'https://github.com/' + owner + '/' + repo
cocom = CoCom(uri=repo_uri, git_path=directory)
items = cocom.fetch()


file1 = open("myfile1.txt","a")


for commit in items:
    print(commit['data']['commit'] + ", ")
    print(commit['data']['AuthorDate'] + ", ")
    print(commit['data']['analysis'] )
    file1.write(commit['data']['commit'] + ", ")
    file1.write(commit['data']['AuthorDate'] + ", ")
    file1.write(json.dumps(commit['data']['analysis']))
    file1.write('\n')
    # with open('vulns.json', 'a') as j:
    #     json.dump(commit, j)
file1.close()
remove_directories()


