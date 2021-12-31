import requests
import os.path
import time
from datetime import datetime
import csv


def get_git_auth_token():
    file = open('../GithubAuthToken.txt', "r")
    return file.read().strip()


def graphql_query_template(query):
    url = 'https://api.github.com/graphql'
    json = {'query': query}
    api_token = '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'#get_git_auth_token()
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

#stars:>=10  created:2001-01-01..2021-01-01 is:public
def get_open_source_repos():
    query = '{ search(query: "is:public created:2011-01-01..2012-01-01 language:java stars:>=10", type: REPOSITORY, first: 100) ' \
            '{repositoryCount nodes { ... on Repository { isFork url stargazerCount pullRequests { totalCount } } } pageInfo { ' \
            'hasNextPage endCursor startCursor } } }'
    repo_urls = []
    extract_open_source_repo_urls(repo_urls, query)
    print("Count " + str(len(repo_urls)))


def extract_open_source_repo_urls(repo_urls, query):
    response = graphql_query_template(query)
    if len(response) > 0:
        search_result = response['data']['search']
        print('Repository count ' + str(search_result['repositoryCount']))
        if len(search_result['nodes']) > 0:
            for repo in search_result['nodes']:
               # repo_urls.append(repo['url'])
                #print(repo['url'])
                #repo_urls.append(repo['url'])
                if not repo['isFork'] and repo['pullRequests']['totalCount'] >= 10 and repo['stargazerCount'] >=10:
                     repo_urls.append(repo['url'])
                     print(repo['url'])
        if search_result['pageInfo']['hasNextPage']:
            end_cursor = search_result['pageInfo']['endCursor']
            query = '{ search(query: "is:public language:java", type: REPOSITORY,' \
                    ' first: 100, after: "%s") ' \
                    '{ repositoryCount nodes { ... on Repository { isFork url stargazerCount pullRequests { totalCount } } } pageInfo { ' \
                    'hasNextPage endCursor startCursor } } }'% (end_cursor)
            extract_open_source_repo_urls(repo_urls, query)


def retrieve_pull_requests_with_details(repository_url):
    pull_request_details = {}
    repo_owner = extract_owner_repo_name_from_url(repository_url)
    query = 'query { repository(name: "%s", owner: "%s") { pullRequests(first: 100) { ' \
            'pageInfo { hasNextPage endCursor } nodes { number id participants { totalCount } reviewThreads(first: ' \
            '100) { totalCount nodes { isResolved } pageInfo { hasNextPage endCursor } } reviews { totalCount } ' \
            'state commits (first: 100) { totalCount nodes { commit { oid committedDate authoredDate} } } createdAt mergedAt merged assignees { totalCount } } } } }'% \
            (repo_owner['repo'], repo_owner['owner'])
    retrieve_pull_request_iteratively(query, repo_owner)


def retrieve_pull_request_iteratively(query, repo_owner):
    response = graphql_query_template(query)
    if len(response) > 0:
        search_result = response['data']['repository']['pullRequests']
        if len(search_result['nodes']) > 0:
            for node in search_result['nodes']:
                if node['participants']['totalCount'] > 1 and node['reviewThreads']['totalCount'] > 0 and \
                        node['reviews']['totalCount'] > 1:
                    for commit_node in node['commits']['nodes']:
                        print('commit hash ' + commit_node['commit']['oid'] + ' commit date ' +
                              commit_node['commit']['committedDate'] + ' authored date ' + commit_node['commit']['authoredDate'])
                    print('pull request ' + str(node['number']))
                    print('created at ' + node['createdAt'])
                    if node['merged']:
                        print('merged at ' + node['mergedAt'])
                # pull_request_details[node['number']] = node
        if search_result['pageInfo']['hasNextPage']:
            end_cursor = search_result['pageInfo']['endCursor']
            query = 'query { repository(name: "%s", owner: "%s") { pullRequests(first: 100, after: "%s") { ' \
                    'pageInfo { hasNextPage endCursor } nodes { number id participants { totalCount } reviewThreads(first: ' \
                    '100) { totalCount nodes { isResolved } pageInfo { hasNextPage endCursor } } reviews { totalCount } ' \
                    'state commits (first: 100) { totalCount nodes { commit { oid committedDate authoredDate} } } createdAt mergedAt merged assignees { totalCount } } } } }' % \
                    (repo_owner['repo'], repo_owner['owner'], end_cursor)
            retrieve_pull_request_iteratively(query, repo_owner)


def extract_owner_repo_name_from_url(url):
    repo_owner_details = url.split('https://github.com/', 1)[1]
    repo_owner = {'owner': repo_owner_details.split('/')[0], 'repo': repo_owner_details.split('/')[1]}
    return repo_owner
