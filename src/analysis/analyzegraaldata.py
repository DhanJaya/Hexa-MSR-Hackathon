import pandas as pd
import json
import csv
import sys

pr_data_df = pd.read_csv('/mnt/d/hackathon/httpiedata1.csv')

df = pd.read_csv('/mnt/d/hackathon/httpie.csv')
pull_requests = df['PullNo'].unique().tolist()

for pull_request in pull_requests:
    pr_data_row = pr_data_df.loc[pr_data_df['PullRequest'] == pull_request]
    all_commits = pr_data_row.iloc[:,5].tolist()
    commit_before_pr = pr_data_row.iloc[:,7].tolist()


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
                if analysis_val['file_path'] in file_analysis:
                    file_analysis[analysis_val['file_path']].append({'commit': commit, 'analysis': analysis_val})
                    break
                else:
                    file_analysis[analysis_val['file_path']] = [{'commit': commit, 'analysis': analysis_val}]
                    break

    for file, analysis_vals in file_analysis.items():
        for analysis_val in analysis_vals:
            print(analysis_val)

    with open('/mnt/d/hackathon/mybatisAnalysis.txt', 'a', newline='') as txt_file:
       # writer = csv.writer(csv_file)
        for file, analysis_vals in file_analysis.items():
            txt_file.write(file + '\n')
            for analysis_val in analysis_vals:
                txt_file.write('\t' + str(analysis_val) + '\n')
        txt_file.write('----------------------------------------------------------\n')
#df_pr = df_groupby_pr.get_group(6961)
#print(df_pr.head())


