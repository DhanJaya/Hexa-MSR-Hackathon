from perceval.backends.core.git import Git


def download_repo():
    # url for the git repo to analyze
    repo_url = 'https://github.com/spring-projects/spring-framework.git'
    # directory for letting Perceval clone the git repo
    repo_dir = 'D:\\PhD\\documents\\MSR2021\\GitRepositories\\spring-framework'

    # create a Git object, pointing to repo_url, using repo_dir for cloning
    repo = Git(repo_url, 'spring', tag='spring')
   # repo.clone
    # fetch all commits as an iterator, and iterate it printing each hash
    for commit in repo.fetch(from_date='2019-01-01'):
        print(commit['data']['commit'])