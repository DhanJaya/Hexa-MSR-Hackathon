import repos.repositories as repositories
import githubapi.apiconnection as apiconnection


def main():
   # repositories.download_repo()
    apiconnection.get_open_source_repos()


if __name__ == "__main__":
    main()
