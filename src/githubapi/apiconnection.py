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
    query = '{ search(query: "is:public stars:>=100 created:2011-01-01..2021-01-01", type: REPOSITORY, first: 100) ' \
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
            query = '{ search(query: "is:public stars:>=100 created:2011-01-01..2021-01-01", type: REPOSITORY,' \
                    ' first: 100, after: "%s") ' \
                    '{ nodes { ... on Repository { isFork url pullRequests { totalCount } } } pageInfo { ' \
                    'hasNextPage endCursor startCursor } } }'% (end_cursor)
            extract_open_source_repo_urls(repo_urls, query)


# def get_cross_reference_issues_for_pr(url):
#     repo_owner = extract_owner_repo_name_from_url(url)
#     pr_cross_ref_event_query = '{ repository(name: "%s", owner: "%s") { pullRequest(number:%s) { timelineItems(first:' \
#                                ' 100, itemTypes: [CONNECTED_EVENT, CROSS_REFERENCED_EVENT]) { pageInfo { hasNextPage' \
#                                ' endCursor } pageCount nodes { ... on ConnectedEvent { source { ... on Issue { url ' \
#                                'bodyHTML comments(first: 100) { nodes { bodyHTML } pageInfo { endCursor hasNextPage } ' \
#                                '} } ... on PullRequest { url bodyHTML comments(first: 100) { nodes { bodyHTML } ' \
#                                'pageInfo { endCursor hasNextPage } } } } } ... on CrossReferencedEvent { source { ...' \
#                                ' on Issue { url bodyHTML comments(first: 100) { nodes { bodyHTML } pageInfo { endCursor' \
#                                ' hasNextPage } } } ... on PullRequest { url bodyHTML comments(first: 100) { nodes { ' \
#                                'bodyHTML } pageInfo { endCursor hasNextPage } } } } } } } } } } ' % (
#                                    repo_owner['repo'], repo_owner['owner'], repo_owner['number'])
#
#     cross_reference_issues = []
#     extract_cross_reference_issues_for_pr(cross_reference_issues, pr_cross_ref_event_query, repo_owner, url)
#     helper.drop_duplicates(cross_reference_issues)
#     return helper.drop_duplicates(cross_reference_issues)
#
#
# def extract_cross_reference_issues_for_pr(cross_reference_issues, pr_cross_ref_event_query, repo_owner, url):
#     response = graphql_query_temp(pr_cross_ref_event_query)
#     time_line_items = response['data']['repository']['pullRequest']['timelineItems']
#     if len(time_line_items['nodes']) > 0:
#         extract_linked_issue_from_response(cross_reference_issues, time_line_items, url)
#     if time_line_items['pageInfo']['hasNextPage']:
#         end_cursor = time_line_items['pageInfo']['endCursor']
#         query = '{ repository(name: "%s", owner: "%s") { pullRequest(number:%s) { timelineItems(first:' \
#                 ' 100, after: "%s", itemTypes: [CONNECTED_EVENT, CROSS_REFERENCED_EVENT]) { pageInfo { hasNextPage' \
#                 ' endCursor } pageCount nodes { ... on ConnectedEvent { source { ... on Issue { url ' \
#                 'bodyHTML comments(first: 100) { nodes { bodyHTML } pageInfo { endCursor hasNextPage } ' \
#                 '} } ... on PullRequest { url bodyHTML comments(first: 100) { nodes { bodyHTML } ' \
#                 'pageInfo { endCursor hasNextPage } } } } } ... on CrossReferencedEvent { source { ...' \
#                 ' on Issue { url bodyHTML comments(first: 100) { nodes { bodyHTML } pageInfo { endCursor' \
#                 ' hasNextPage } } } ... on PullRequest { url bodyHTML comments(first: 100) { nodes { ' \
#                 'bodyHTML } pageInfo { endCursor hasNextPage } } } } } } } } } } ' % (
#                     repo_owner['repo'], repo_owner['owner'], repo_owner['number'], end_cursor)
#         extract_cross_reference_issues_for_pr(cross_reference_issues, query, repo_owner, url)