import csv

import githubapi.apiconnection as apiconnection
import analysis.codecomplexityanalysis as cocom_analysis


def main():
    repo_urls = apiconnection.get_open_source_repos()
    #repo_urls = ['https://github.com/apache/tomcat', 'https://github.com/apache/curator', 'https://github.com/Netflix/genie', 'https://github.com/eclipse/jetty.project', 'https://github.com/google/hover', 'https://github.com/GoogleCloudPlatform/community']
    for url in repo_urls:
        pull_request_details = apiconnection.retrieve_pull_requests_with_details(url)
        if len(pull_request_details) > 0:
            for number, detail in pull_request_details.items():
                #get start date and end date of commits and pass to the cocom analysis
                start_date = list(detail['commits'].values())[0]['commit_date']
                end_date = list(detail['commits'].values())[-1]['commit_date']

                commit_analysis = cocom_analysis.run_graal_analysis(url, start_date, end_date, detail['commits'].keys())
                if commit_analysis is not None and len(commit_analysis) > 0:
                    for commit, analysis in commit_analysis.items():
                        append_to_file(url, number, commit,  analysis)


def append_to_file(url, pr_number, commit_hash, analysis):
    with open('myfile4.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([url, pr_number, commit_hash, analysis])


if __name__ == "__main__":
    main()
