import requests
import os.path
import time
import datetime
import csv
import util.helper as help


def get_git_auth_token():
    file = open('/mnt/d/PhD/workspace/PycharmProjects/Hexa-MSR-Hackathon/GithubAuthToken.txt', "r")
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
    query = '{ search(query: "is:public created:2011-01-01..2012-01-01 language:java stars:>=10", type: REPOSITORY, first: 100) ' \
            '{repositoryCount nodes { ... on Repository { isFork url stargazerCount pullRequests { totalCount } } } pageInfo { ' \
            'hasNextPage endCursor startCursor } } }'
    repo_urls = []
    extract_open_source_repo_urls(repo_urls, query)
    print("Count " + str(len(repo_urls)))
    return repo_urls


def extract_open_source_repo_urls(repo_urls, query):
    response = graphql_query_template(query)
    if len(response) > 0:
        search_result = response['data']['search']
        print('Repository count ' + str(search_result['repositoryCount']))
        if len(search_result['nodes']) > 0:
            for repo in search_result['nodes']:
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
    repo_owner = help.extract_owner_repo_name_from_url(repository_url)
    query = 'query { repository(name: "%s", owner: "%s") { pullRequests(first: 100, states: MERGED) { ' \
            'pageInfo { hasNextPage endCursor } nodes { number id participants { totalCount }' \
            'comments { totalCount } reviews { totalCount } reviewDecision ' \
            ' commits (first: 100) { totalCount nodes { commit { oid committedDate authoredDate} } } ' \
            ' headRepository { url } createdAt} } } }'% \
            (repo_owner['repo'], repo_owner['owner'])
    retrieve_pull_request_iteratively(query, repo_owner, pull_request_details)
    return pull_request_details


def retrieve_pull_request_iteratively(query, repo_owner, pull_request_details):
    response = graphql_query_template(query)
    if response is not None and len(response) > 0:
        search_result = response['data']['repository']['pullRequests']
        if len(search_result['nodes']) > 0:
            for node in search_result['nodes']:
                if node['participants']['totalCount'] > 1 and (node['reviews']['totalCount'] >= 2 or
                                                               node['comments']['totalCount'] >= 2):
                    if len(node['commits']['nodes']) > 2 and len(node['commits']['nodes']) < 100 :
                        commits = {}
                        if node['headRepository'] is not None and node['headRepository']['url'] is not None:# and node['reviewDecision'] == 'APPROVED':
                            print('headRepository ' + node['headRepository']['url'])
                            print('pull request ' + str(node['number']) + ' pr created on ' + node['createdAt'])
                            pr_created = datetime.datetime.strptime(node['createdAt'], "%Y-%m-%dT%H:%M:%SZ")
                            commit_before_pr = None
                            for commit_node in node['commits']['nodes']:
                                print('commit hash ' + commit_node['commit']['oid'] + ' commit date ' +
                                      commit_node['commit']['committedDate'] + ' authored date ' +
                                      commit_node['commit']['authoredDate'] + ' participants '
                                      + str(node['participants']['totalCount']))

                                commits[commit_node['commit']['oid']] = {'commit_date' :
                                                                        commit_node['commit']['committedDate'],
                                                                        'author_date':commit_node['commit']['authoredDate']}
                                if commit_before_pr is None:
                                    commit_before_pr = commit_node['commit']['oid']
                                elif datetime.datetime.strptime(commit_node['commit']['committedDate'], "%Y-%m-%dT%H:%M:%SZ") < pr_created:
                                    commit_before_pr = commit_node['commit']['oid']

                            pull_request_details[node['number']] = {'number': node['number'], 'headRepository':
                                node['headRepository']['url'], 'commits': commits, 'participants':
                                node['participants']['totalCount'], 'prCreated':  node['createdAt'], 'commitBeforePR': commit_before_pr}



        if search_result['pageInfo']['hasNextPage']:
            end_cursor = search_result['pageInfo']['endCursor']
            query = 'query { repository(name: "%s", owner: "%s") { pullRequests(first: 100, states: MERGED, after: "%s") { ' \
                    'pageInfo { hasNextPage endCursor } nodes { number id participants { totalCount }' \
                    'comments { totalCount } reviews { totalCount } reviewDecision ' \
                    ' commits (first: 100) { totalCount nodes { commit { oid committedDate authoredDate} } } ' \
                    ' headRepository { url } createdAt} } } }' % \
                    (repo_owner['repo'], repo_owner['owner'], end_cursor)
            retrieve_pull_request_iteratively(query, repo_owner, pull_request_details)



