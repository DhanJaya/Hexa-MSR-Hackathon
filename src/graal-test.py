import json
import os
import shutil

from graal.backends.core.covuln import CoVuln

repo_uri = "http://github.com/chaoss/grimoirelab-perceval"
directory = "/tmp/grimoirelab-perceval"

if os.path.exists(directory):
    shutil.rmtree(directory)

repo_dir = "/tmp/grimoirelab-perceval"

cc = CoVuln(uri=repo_uri, entrypoint="perceval", git_path=repo_dir)

items = cc.fetch()
for commit in items:
    print(commit['data']['analysis'])
    with open('vulns.json', 'a') as j:
        json.dump(commit, j)
