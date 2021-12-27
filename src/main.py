import repos.repositories as repositories
import githubapi.apiconnection as apiconnection


def main():

   # repositories.download_repo()
    #apiconnection.get_open_source_repos()
    apiconnection.retrieve_pull_requests_with_details('https://github.com/stanfordnlp/stanza')


if __name__ == "__main__":
    main()
