import os
from git import Repo, InvalidGitRepositoryError, GitCommandError

main_path = os.path.dirname(os.path.abspath(__file__))
backup_main_path = "/home/howler1/.backups"

# get config data
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
print(config["remote_name"])
