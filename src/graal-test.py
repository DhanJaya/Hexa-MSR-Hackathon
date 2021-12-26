import json
import os
import shutil

from graal.backends.core.covuln import CoVuln

owner = 'chaoss'
repo = 'grimoirelab-graal'
directory = '/tmp/' + repo

if os.path.exists(directory):
    shutil.rmtree(directory)

repo_uri = 'https://github.com/' + owner + '/' + repo
co_vuln = CoVuln(uri=repo_uri, entrypoint='/tmp/worktrees/'+repo, git_path=directory)
items = co_vuln.fetch()
for commit in items:
    print(commit['data']['analysis'])
    with open('vulns.json', 'a') as j:
        json.dump(commit, j)
