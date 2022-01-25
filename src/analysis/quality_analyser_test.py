import datetime
import os
import shutil

from graal.backends.core.coqua import CoQua, CATEGORY_COQUA_FLAKE8, CATEGORY_COQUA_PYLINT
from graal.backends.core.covuln import CoVuln


def remove_directories(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print('Removed: ' + directory)
    if os.path.exists('/tmp/worktrees'):
        shutil.rmtree('/tmp/worktrees')
        print('Removed: /tmp/worktrees')


def run_quality_analysis():
    repo = 'flask'
    directory = '/tmp/' + repo
    repo_uri = 'https://github.com/r0fls/flask'

    remove_directories(directory)

    start_date_time = datetime.datetime.strptime('2017-01-16T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ') - datetime.timedelta(2)
    end_date_time = datetime.datetime.strptime('2017-01-17T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(days=2)

    # Entrypoint should be the source root (Usually source root = repo name)
    coqua = CoVuln(uri=repo_uri, entrypoint='/tmp/worktrees/flask', git_path=directory)
    items = coqua.fetch(from_date=start_date_time, to_date=end_date_time)

    for commit in items:
        print(commit)
    remove_directories(directory)


run_quality_analysis()
