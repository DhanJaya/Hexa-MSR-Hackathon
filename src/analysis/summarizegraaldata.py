import pandas as pd
import csv
import os

def complexcity_summary():
    df = pd.read_csv('D:/hackathon/KerasAnalysis.csv')
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

        file_exist = os.path.exists('D:/hackathon/kerasComplexitySummary.csv')

        with open('D:/hackathon/kerasComplexitySummary.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if not file_exist:
                writer.writerow(['URL', 'PullNo', 'Participants', 'CCN', 'LOC', 'Tokens', 'Functions'])
           # for pr, results in results_for_csv.items():
            writer.writerow([url, pull_request, participants, avg_ccn, avg_loc, avg_tokens, avg_function])


def quality_summary():
    pr_data_df = pd.read_csv('D:/hackathon/pandas-prs.csv')
    df = pd.read_csv('D:/hackathon/Quality/pandasquality.csv')
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


        file_exist = os.path.exists('D:/hackathon/Quality/pandasQualitySummary.csv')

        with open('D:/hackathon/Quality/pandasQualitySummary.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if not file_exist:
                writer.writerow(['URL', 'PullNo', 'Participants', 'Quality'])
            writer.writerow(
                    [url, pull_request, participants, quality_diff])


def vulnerability_summary():

    pr_data_df = pd.read_csv('D:/hackathon/httpie-prs.csv')
    df = pd.read_csv('D:/hackathon/vulnerability/httpie-vulnerabilities.csv')
    pull_requests = df['pr'].unique().tolist()

    for pull_request in pull_requests:
        pr_data_row = pr_data_df.loc[pr_data_df['PullRequest'] == pull_request]  # df.iat[0,0]
        print(pr_data_row)

        participants = pr_data_row.iat[0, 8]

        # URL,PullNo,Participants,CommitHash,Analysis
        pull_request_change = df.loc[df['pr'] == pull_request]
        analysis_columns = pull_request_change['analysis'].tolist()
        commits_columns = pull_request_change['commit_hash'].tolist()
        url = pull_request_change['repo'].tolist()[0]

        start_index = 0
        if 'num_vulns' not in analysis_columns[0]:
            for index in range(len(analysis_columns)):
                if 'num_vulns' in analysis_columns[index]:
                    start_index = index
                    break

        vuln_at_start = eval(analysis_columns[start_index])['num_vulns']
        vuln_at_end = eval(analysis_columns[-1])['num_vulns']
        vuln_diff = (float(vuln_at_start) - float(vuln_at_end))


        file_exist = os.path.exists('D:/hackathon/vulnerability/httpieVulnSummary.csv')

        with open('D:/hackathon/vulnerability/httpieVulnSummary.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if not file_exist:
                writer.writerow(['URL', 'PullNo', 'Participants', 'Num_Vulns'])
            writer.writerow(
                [url, pull_request, participants, vuln_diff])


def grouped_summary():
    vuln_df = pd.read_csv('D:/hackathon/vulnerability/scikitlearnVulnSummary.csv')
    complexity_df = pd.read_csv('D:/hackathon/complexity/scikitlearnComplexitySummary.csv')
    quality_df = pd.read_csv('D:/hackathon/Quality/scikitlearnQualitySummary.csv')


    quality_pull_requests = quality_df['PullNo'].tolist()
    complexity_pull_requests = complexity_df['PullNo'].tolist()
    vuln_pull_requests = vuln_df['PullNo'].tolist()

    ccn = complexity_df['CCN'].tolist()
    quality = quality_df['Quality'].tolist()
    num_vuln = vuln_df['Num_Vulns'].tolist()

    participants = quality_df['Participants'].tolist()
    url = quality_df['URL'].tolist()


    for quality_pull_request in quality_pull_requests:
        if quality_pull_request in complexity_pull_requests and quality_pull_request in vuln_pull_requests:
            quality_index = quality_pull_requests.index(quality_pull_request)
            complexity_index = complexity_pull_requests.index(quality_pull_request)
            vuln_index = vuln_pull_requests.index(quality_pull_request)

            file_exist = os.path.exists('D:/hackathon/Summary/scikitlearnSummary.csv')

            with open('D:/hackathon/Summary/scikitlearnSummary.csv', 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                if not file_exist:
                    writer.writerow(['URL', 'PullNo', 'Participants', 'CCN', 'Quality', 'Num_Vulns'])
                writer.writerow(
                    [url[quality_index], quality_pull_request, participants[quality_index], ccn[complexity_index],
                    quality[quality_index], num_vuln[vuln_index]])





#quality_summary()
#complexcity_summary()
#vulnerability_summary()
grouped_summary()