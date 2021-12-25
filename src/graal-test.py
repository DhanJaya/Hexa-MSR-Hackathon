import json
import os
import shutil

from graal.backends.core.covuln import CoVuln

repo_uri = "https://github.com/chaoss/grimoirelab-perceval"
directory = "/tmp/grimoirelab-perceval"

# The repository should be mirrored to a new directory.
# If the repository already exists in the given path it won't be mirrored.
# As a result of the above the worktree won't be crated.
if os.path.exists(directory):
    shutil.rmtree(directory)

repo_dir = "/tmp/grimoirelab-perceval"

# Entry point should be one of the modules in the project that we need to analyse, for example src/main
co_vuln = CoVuln(uri=repo_uri, entrypoint="perceval", git_path=repo_dir)

items = co_vuln.fetch()
for commit in items:
    print(commit['data']['analysis'])
    with open('vulns.json', 'a') as j:
        json.dump(commit, j)
