import requests
import os.path
import time
from datetime import datetime


def get_git_auth_token():
    file = open('../GithubAuthToken.txt', "r")
    return file.read().strip()


def graphql_query_template(query):
    url = 'https://api.github.com/graphql'
    json = {'query': query}
    api_token = get_git_auth_token()
    headers = {'Authorization': 'token %s' % api_token}
    no_of_tries = 0
    try:
        no_of_tries +=1
        request = requests.post(url=url, json=json, headers=headers)
        if request.status_code == 200:
            return request.json()
        elif no_of_tries > 2:
            print("Failed request: " + str(request.status_code))
            raise Exception("Request cannot be processed ")
        else:
            print("Retrying request in 5 seconds")
            time.sleep(5)
            graphql_query_template(query)

    except Exception as exception:
        if no_of_tries > 2:
            raise Exception("request cannot be processed {}".format(exception))
        else:
            print("Exception occurred retry in 5 seconds {}".format(exception))
            time.sleep(5)


def get_open_source_repos():
    query = '{ search(query: "is:public stars:>=100 created:2011-01-01..2021-01-01 languages:Python", type: REPOSITORY, first: 100) ' \
            '{ nodes { ... on Repository { isFork url pullRequests { totalCount } } } pageInfo { ' \
            'hasNextPage endCursor startCursor } } }'
    repo_urls = []
    extract_open_source_repo_urls(repo_urls, query)


def extract_open_source_repo_urls(repo_urls, query):
    response = graphql_query_template(query)
    if len(response) > 0:
        search_result = response['data']['search']
        if len(search_result['nodes']) > 0:
            for repo in search_result['nodes']:
                if not repo['isFork'] and repo['pullRequests']['totalCount'] >= 10:
                    repo_urls.append(repo['url'])
                    print(repo['url'])
        if search_result['pageInfo']['hasNextPage']:
            end_cursor = search_result['pageInfo']['endCursor']
            query = '{ search(query: "is:public stars:>=100 created:2011-01-01..2021-01-01 languages:Python", type: REPOSITORY,' \
                    ' first: 100, after: "%s") ' \
                    '{ nodes { ... on Repository { isFork url pullRequests { totalCount } } } pageInfo { ' \
                    'hasNextPage endCursor startCursor } } }'% (end_cursor)
            extract_open_source_repo_urls(repo_urls, query)


def retrieve_pull_requests_with_details(repository_url):
    pull_request_details = {}
    repo_owner = extract_owner_repo_name_from_url(repository_url)
    query = 'query { repository(name: "%s", owner: "%s") { pullRequests(first: 100) { ' \
            'pageInfo { hasNextPage endCursor } nodes { number id participants { totalCount } reviewThreads(first: ' \
            '100) { totalCount nodes { isResolved } pageInfo { hasNextPage endCursor } } reviews { totalCount } ' \
            'state commits { totalCount } createdAt mergedAt merged assignees { totalCount } } } } }'% \
            (repo_owner['repo'], repo_owner['owner'])
    response = graphql_query_template(query)
    if len(response) > 0:
        search_result = response['data']['repository']['pullRequests']
        if len(search_result['nodes']) > 0:
            for node in search_result['nodes']:
                pull_request_details[node['number']] = node
                print(pull_request_details[node['number']])





def extract_owner_repo_name_from_url(url):
    repo_owner_details = url.split('https://github.com/', 1)[1]
    repo_owner = {'owner': repo_owner_details.split('/')[0], 'repo': repo_owner_details.split('/')[1]}
    return repo_owner
