import pandas as pd
import csv
import os

def complexcity_summary():
    df = pd.read_csv('D:/hackathon/scikitlearnAnalysis.csv')
    pull_requests = df['PullNo'].unique().tolist()
    for pull_request in pull_requests:
        pull_request_change = df.loc[df['PullNo'] == pull_request]
        ccn_columns = pull_request_change['CCN'].tolist()
        loc_columns = pull_request_change['LOC'].tolist()
        token_columns = pull_request_change['Tokens'].tolist()
        function_columns = pull_request_change['Functions'].tolist()
        participants = pull_request_change['Participants'].tolist()[0]
        url = pull_request_change['URL'].tolist()[0]

        avg_ccn = None
        avg_loc = None
        avg_tokens = None
        avg_function = None
        results_for_csv = {}
        if len(ccn_columns) > 1:
            total_rows = len(ccn_columns)

            sum_ccn = sum(ccn_columns)
            avg_ccn =sum_ccn/total_rows
            avg_loc = sum(loc_columns) / total_rows
            avg_tokens = sum(token_columns) / total_rows
            avg_function = sum(function_columns) / total_rows
        else:
            avg_ccn = ccn_columns[0]
            avg_loc = loc_columns[0]
            avg_tokens = token_columns[0]
            avg_function = function_columns[0]
        #results_for_csv[pull_request] = {'ccn': avg_ccn, 'ccn': avg_ccn, 'loc': avg_loc, 'tokens': avg_tokens, 'funs': avg_function}

        file_exist = os.path.exists('D:/hackathon/scikitlearnComplexitySummary.csv')

        with open('D:/hackathon/scikitlearnComplexitySummary.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if not file_exist:
                writer.writerow(['URL', 'PullNo', 'Participants', 'CCN', 'LOC', 'Tokens', 'Functions'])
           # for pr, results in results_for_csv.items():
            writer.writerow([url, pull_request, participants, avg_ccn, avg_loc, avg_tokens, avg_function])


def quality_summary():
    pr_data_df = pd.read_csv('D:/hackathon/tornado-prs.csv')
    df = pd.read_csv('D:/hackathon/Quality/tornadoquality.csv')
    pull_requests = df['PullNo'].unique().tolist()

    for pull_request in pull_requests:
        pr_data_row = pr_data_df.loc[pr_data_df['PullRequest'] == pull_request]  # df.iat[0,0]
        print(pr_data_row)
        all_commits = list(eval(pr_data_row.iat[0, 5]))
        commit_before_pr = pr_data_row.iat[0, 7]

                #URL,PullNo,Participants,CommitHash,Analysis
        pull_request_change = df.loc[df['PullNo'] == pull_request]
        analysis_columns = pull_request_change['Analysis'].tolist()
        commits_columns = pull_request_change['CommitHash'].tolist()
        url = pull_request_change['URL'].tolist()[0]
        participants = pull_request_change['Participants'].tolist()[0]

        index = commits_columns.index(commit_before_pr)

        quality_at_start = eval(analysis_columns[index].replace('null', '0'))['quality']
        quality_at_end = eval(analysis_columns[-1].replace('null', '0'))['quality']
        quality_diff = (float(quality_at_end) - float(quality_at_start))


        file_exist = os.path.exists('D:/hackathon/tornadoQualitySummary.csv')

        with open('D:/hackathon/tornadoQualitySummary.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if not file_exist:
                writer.writerow(['URL', 'PullNo', 'Participants', 'Quality'])
            writer.writerow(
                    [url, pull_request, participants, quality_diff])


quality_summary()