import csv

import githubapi.apiconnection as apiconnection
import analysis.codecomplexityanalysis as cocom_analysis


def main():
    #repo_urls = apiconnection.get_open_source_repos()
    repo_urls = ['https://github.com/spring-projects/spring-boot', 'https://github.com/elastic/elasticsearch', 'https://github.com/ReactiveX/RxJava', 'https://github.com/google/guava', 'https://github.com/apache/tomcat', 'https://github.com/dbeaver/dbeaver', 'https://github.com/greenrobot/EventBus', 'https://github.com/SeleniumHQ/selenium', 'https://github.com/google/gson', 'https://github.com/jenkinsci/jenkins', 'https://github.com/redisson/redisson', 'https://github.com/apache/flink', 'https://github.com/mybatis/mybatis-3', 'https://github.com/oracle/graal']
    for url in repo_urls:
        pull_request_details = apiconnection.retrieve_pull_requests_with_details(url)
        if len(pull_request_details) > 0:
            for number, detail in pull_request_details.items():
                #get start date and end date of commits and pass to the cocom analysis
                start_date = list(detail['commits'].values())[0]['commit_date']
                end_date = list(detail['commits'].values())[-1]['commit_date']
                participants = detail['participants']
                review_threads = detail['reviewThreads']
                total_reviews = detail['totalReviews']
                commit_analysis = cocom_analysis.run_graal_analysis(url, start_date, end_date, detail['commits'].keys())
                if commit_analysis is not None and len(commit_analysis) > 0:
                    for commit, analysis in commit_analysis.items():
                        append_to_file(url, number, participants, review_threads, total_reviews, commit,  analysis)


def append_to_file(url, pr_number, participants, review_threads, total_reviews, commit_hash, analysis):
    with open('/mnt/d/hackathon/myfile1.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([url, pr_number, participants, review_threads, total_reviews, commit_hash, analysis])


if __name__ == "__main__":
    main()
