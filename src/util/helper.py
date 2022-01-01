def extract_owner_repo_name_from_url(url):
    repo_owner_details = url.split('https://github.com/', 1)[1]
    repo_owner = {'owner': repo_owner_details.split('/')[0], 'repo': repo_owner_details.split('/')[1]}
    return repo_owner