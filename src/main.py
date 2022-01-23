import csv
import os
import pandas as pd

import githubapi.apiconnection as apiconnection
import analysis.codecomplexityanalysis as cocom_analysis

file_path = 'data/prs/flask-prs.csv'

def retreive_pr_details():
    #repo_urls = apiconnection.get_open_source_repos()
    #repo_urls = ['https://github.com/spring-projects/spring-boot', 'https://github.com/elastic/elasticsearch', 'https://github.com/ReactiveX/RxJava', 'https://github.com/google/guava', 'https://github.com/apache/tomcat', 'https://github.com/dbeaver/dbeaver', 'https://github.com/greenrobot/EventBus', 'https://github.com/SeleniumHQ/selenium', 'https://github.com/google/gson', 'https://github.com/jenkinsci/jenkins', 'https://github.com/redisson/redisson', 'https://github.com/apache/flink', 'https://github.com/mybatis/mybatis-3', 'https://github.com/oracle/graal']
    #repo_urls = ['https://github.com/httpie/httpie']
    #repo_urls = ['https://github.com/pallets/flask']
    #repo_urls = ['https://github.com/tornadoweb/tornado']
    repo_urls = ['https://github.com/keras-team/keras']


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

                add_pr_details_to_csv(url, number, head_repository, start_date, end_date, commits, pr_created, commit_before_pr, participants)


def run_graal_analysis():
    already_processed = []
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        already_processed.extend(df['PullNo'].unique().tolist())
    with open(file_path, encoding="utf8") as f:
        csv_reader = csv.DictReader(f)
        # skip the header
        next(csv_reader)
        # show the data
        for line in csv_reader:
            if int(line['PullRequest']) not in already_processed:
                print(f"Processing PR {line['PullRequest']} in  {line['Fork']} ")
                commit_analysis = cocom_analysis.run_graal_analysis(line['Fork'], line['Start_date'], line['End_date'],
                                                                    line['Commits'])
                if commit_analysis is not None and len(commit_analysis) > 0:
                    for commit, analysis in commit_analysis.items():
                         append_to_file(line['Repo'], line['PullRequest'], line['Participants'], commit, analysis)


def add_pr_details_to_csv(repo, pr_no, fork, start_date, end_date, commits, pr_created, commit_before_pr, participants):
    file_exist = os.path.exists(file_path)
    with open(file_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        if not file_exist:
            writer.writerow(['Repo', 'PullRequest', 'Fork', 'Start_date', 'End_date', 'Commits', 'PR_Start', 'Commit_Before_PR', 'Participants'])
        writer.writerow([repo, pr_no, fork, start_date, end_date, commits, pr_created, commit_before_pr, participants])


def append_to_file(url, pr_number, participants, commit_hash, analysis):
    file_exist = os.path.exists(file_path)
    with open(file_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        if not file_exist:
            writer.writerow(['URL', 'PullNo', 'Participants', 'CommitHash', 'Analysis'])
        writer.writerow([url, pr_number, participants, commit_hash, analysis])


if __name__ == "__main__":
   retreive_pr_details()
   run_graal_analysis()
