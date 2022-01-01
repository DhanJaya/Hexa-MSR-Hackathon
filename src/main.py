import repos.repositories as repositories
import githubapi.apiconnection as apiconnection
import analysis.codecomplexityanalysis as cocom_analysis


def main():
    repo_urls = apiconnection.get_open_source_repos()
    for url in repo_urls:
        pull_request_details = apiconnection.retrieve_pull_requests_with_details(url)
        if len(pull_request_details) > 0:
            for number, detail in pull_request_details.items():
                #get start date and end date of commits and pass to the cocom analysis
                start_date = detail['commits'][0]['commit_date']
                number_of_commits = len(detail['commits'])
                end_date = detail['commits'][number_of_commits - 1]['commit_date']
                cocom_analysis.run_graal_analysis(url, start_date, end_date)


if __name__ == "__main__":
    main()
