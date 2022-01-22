import pandas as pd
import json
import csv
import sys

pr_data_df = pd.read_csv('/mnt/d/hackathon/flaskprdata.csv')

df = pd.read_csv('/mnt/d/hackathon/flask.csv')
pull_requests = df['PullNo'].unique().tolist()

for pull_request in pull_requests:
    pr_data_row = pr_data_df.loc[pr_data_df['PullRequest'] == pull_request]#df.iat[0,0]
    print(pr_data_row)
    all_commits = list(eval(pr_data_row.iat[0,5]))
    commit_before_pr = pr_data_row.iat[0,7]

    commits_before_pr = []
    for all_commit in all_commits:
        if commit_before_pr == all_commit:
            commits_before_pr.append(all_commit)
            break
        else:
            commits_before_pr.append(all_commit)

    pull_request_change = df.loc[df['PullNo'] == pull_request]
    analysis_columns = pull_request_change['Analysis'].tolist()
    commit_hash_columns = pull_request_change['CommitHash'].tolist()

    file_analysis = {}
    index = 0
    for analysis_column in analysis_columns:
        commit = commit_hash_columns[index]
        index +=1
        analysis_column = analysis_column.replace('null', '""')
        res = list(eval(analysis_column))
        for analysis_val in res:
            if 'ext' in analysis_val and analysis_val['ext'] == 'py':
                print(analysis_val['file_path'])
                if analysis_val['file_path'] in file_analysis:
                    file_analysis[analysis_val['file_path']].append({'commit': commit, 'analysis': analysis_val})
                else:
                    file_analysis[analysis_val['file_path']] = [{'commit': commit, 'analysis': analysis_val}]
    print(file_analysis)
    filtered_analysis = {}
    if len(commits_before_pr) > 0:
        for file, analysis_vals in file_analysis.items():
            analysis_list = []
            for analysis in analysis_vals:
                if analysis['commit'] in commits_before_pr:
                    analysis_list = [analysis]
                else:
                    analysis_list.append(analysis)
            filtered_analysis[file] = analysis_list
    else:
        filtered_analysis = file_analysis
    print(filtered_analysis)
    with open('/mnt/d/hackathon/flaskAnalysis.txt', 'a', newline='') as txt_file:
       # writer = csv.writer(csv_file)
        txt_file.write(
           '------------------------------------------------------------------------------------------------------\n')
        txt_file.write('Pull Request ' + str(pull_request) + '\n')
        for file, analysis_vals in filtered_analysis.items():
            txt_file.write(file + '\n')
            for analysis_val in analysis_vals:
                txt_file.write('\t' + str(analysis_val['commit']) + ' ' +str(analysis_val['analysis']) + '\n')




