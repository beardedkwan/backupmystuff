import os
from git import Repo, InvalidGitRepositoryError, GitCommandError

main_path = os.path.dirname(os.path.abspath(__file__))
backup_main_path = "/home/howler1/.backups"

def parse_config_file():
    config = {}
    try:
        with open(f"{main_path}/backupmystuff.conf", "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("'\"")

                    config[key] = value
    except FileNotFoundError:
        print("No config file found.")
    except IOError:
        print("Unable to read config file.")

    return config

# Check if config file exists
config = parse_config_file()
if config and len(config) > 0 and "remote_name" in config and "remote_url" in config:
    try:
        # Initialize backups git repository
        try:
            repo = Repo(backup_main_path)

        except InvalidGitRepositoryError:
            print("Initializing a new Git repository...")
            repo = Repo.init(backup_main_path)

        # Add a remote
        remote_name = config["remote_name"]
        remote_url = config["remote_url"]

        if remote_name not in repo.remotes:
            repo.create_remote(remote_name, remote_url)
            print(f"Added remote '{remote_name}' with URL '{remote_url}'.")

        # Stage changes
        repo.index.add("*")

        # Commit changes if there are any
        if repo.index.diff("HEAD"):
            repo.index.commit("Automated backup")
            print("Changes committed.")

        else:
            print("No changes to commit.")

        # Push to remote repo
        remote = repo.remote(name=remote_name)
        remote.push()

        print("Successfully pushed to remote repository.")

    except GitCommandError as e:
        print(f"Git command error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

else:
    print("Missing config file or required keys to push to remote repository.")
