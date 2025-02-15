import os
from git import Repo, InvalidGitRepositoryError

main_path = os.path.dirname(os.path.abspath(__file__))

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

config = parse_config_file()

# Check if config file exists
config = parse_config_file()
if len(config) > 0:
    # Initialize backups git repository
    repo = Repo(main_path)

    if os.path.isdir(os.path.join(main_path, ".git")):
        print("Git repository successfully initialized.")
    else:
        print("Failed to initialize Git repository.")

    # Add a remote
    remote_name = config["remote_name"]
    remote_url = config["remote_url"]

    if remote_name not in repo.remotes:
        repo.create_remote(remote_name, remote_url)

    # Stage and commit changes
    repo.index.add("*")
    repo.index.commit(f"Automated backup")

    # Push to remote repo
    remote = repo.remote(name=remote_name)
    remote.push()

    print("Successfully pushed to remote repository.")
