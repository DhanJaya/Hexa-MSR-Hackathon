import csv
import os
import pandas as pd

import githubapi.apiconnection as apiconnection
import analysis.codecomplexityanalysis as cocom_analysis
import analysis.codequalityanalysis as coqua_analysis

file_path = 'data/prs/flask-prs.csv'


def retreive_pr_details():
    # repo_urls = apiconnection.get_open_source_repos()

    #repo_urls = ['https://github.com/httpie/httpie']

    #repo_urls = ['https://github.com/pallets/flask']
    repo_urls = ['https://github.com/tornadoweb/tornado']
    #repo_urls = ['https://github.com/pallets/flask']

    #repo_urls = ['https://github.com/keras-team/keras']
    # repo_urls = ['https://github.com/ansible/ansible']
    #repo_urls = ['https://github.com/psf/requests']
    #repo_urls = ['https://github.com/scrapy/scrapy']

    for url in repo_urls:
        pull_request_details = apiconnection.retrieve_pull_requests_with_details(url)
        if len(pull_request_details) > 0:
            for number, detail in pull_request_details.items():
                #get start date and end date of commits and pass to the cocom analysis
                start_date = list(detail['commits'].values())[0]['commit_date']
                end_date = list(detail['commits'].values())[-1]['commit_date']
                participants = detail['participants']
                head_repository = detail['headRepository']
                commits = list(detail['commits'].keys())
                pr_created = detail['prCreated']
                commit_before_pr = detail['commitBeforePR']
                file_paths = detail['filePaths']

                add_pr_details_to_csv(url, number, head_repository, start_date, end_date, commits, pr_created,
                                      commit_before_pr, participants, file_paths)


def get_most_used_module_name(file_paths):
    modules = {}
    file_path_list = list(eval(file_paths))
    for file_path_name in file_path_list:
        if '/' in file_path_name:
            module_name = file_path_name.split('/')[0]
            if module_name not in ['test', 'tests', 'doc', 'docs']:
                if module_name in modules:
                    value = modules[module_name]
                    value += 1
                    modules[module_name] = value
                else:
                    modules[module_name] = 1
    most_used_module = None
    most_used_time = 0
    for module, number in modules.items():
        if number > most_used_time:
            most_used_module = module
            most_used_time = number
    return most_used_module

def run_quality_analysis():
    already_processed = []
    if os.path.exists('/mnt/d/hackathon/test.csv'):
        df = pd.read_csv('/mnt/d/hackathon/test.csv')
        already_processed.extend(df['PullNo'].unique().tolist())
    with open('/mnt/d/hackathon/httpie-prs.csv', encoding="utf8") as f:
        csv_reader = csv.DictReader(f)
        # skip the header
        next(csv_reader)
        # show the data
        for line in csv_reader:
            if line['Run_Analysis'] == 'true':
            #if int(line['PullRequest']):
                print(f"Processing PR {line['PullRequest']} in  {line['Fork']} ")
                module_name = get_most_used_module_name(line['File_Paths'])
                commit_analysis = coqua_analysis.run_quality_analysis(line['Fork'], line['Start_date'],
                                                                       line['End_date'],
                                                                       line['Commits'], module_name)
                if commit_analysis is not None and len(commit_analysis) > 0:
                    for commit, analysis in commit_analysis.items():
                        append_to_file('/mnt/d/hackathon/kerasquality.csv', line['Repo'], line['PullRequest'],
                                       line['Participants'], commit, analysis)


def run_complexity_analysis():
    already_processed = []
    if os.path.exists('/mnt/d/hackathon/scrapy.csv'):
        df = pd.read_csv('/mnt/d/hackathon/scrapy.csv')
        already_processed.extend(df['PullNo'].unique().tolist())
    with open('/mnt/d/hackathon/scrapyprdata.csv', encoding="utf8") as f:
        csv_reader = csv.DictReader(f)
        # skip the header
        next(csv_reader)
        # show the data
        for line in csv_reader:
            #scrapy stopped at 1887
            if int(line['PullRequest']) > 1886:
                print(f"Processing PR {line['PullRequest']} in  {line['Fork']} ")
                commit_analysis = cocom_analysis.run_graal_analysis(line['Fork'], line['Start_date'], line['End_date'],
                                                                    line['Commits'])
                if commit_analysis is not None and len(commit_analysis) > 0:
                    for commit, analysis in commit_analysis.items():
                        append_to_file('/mnt/d/hackathon/scrapy.csv', line['Repo'], line['PullRequest'],
                                       line['Participants'], commit, analysis)


def add_pr_details_to_csv(repo, pr_no, fork, start_date, end_date, commits, pr_created, commit_before_pr, participants, file_paths):
    file_exist = os.path.exists('/mnt/d/hackathon/tornado-prs.csv')
    with open('/mnt/d/hackathon/tornado-prs.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        if not file_exist:
            writer.writerow(
                ['Repo', 'PullRequest', 'Fork', 'Start_date', 'End_date', 'Commits', 'PR_Start', 'Commit_Before_PR',
                 'Participants', 'File_Paths', 'Run_Analysis'])
        writer.writerow([repo, pr_no, fork, start_date, end_date, commits, pr_created, commit_before_pr, participants, file_paths, 'false'])


def append_to_file(file, url, pr_number, participants, commit_hash, analysis):
    file_exist = os.path.exists(file)
    with open(file, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        if not file_exist:
            writer.writerow(['URL', 'PullNo', 'Participants', 'CommitHash', 'Analysis'])
        writer.writerow([url, pr_number, participants, commit_hash, analysis])


if __name__ == "__main__":
    #retreive_pr_details()
    #run_complexity_analysis()
    run_quality_analysis()
