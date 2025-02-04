from pathlib import Path
import getpass
import shutil

# Get logged in user for directory paths
user = getpass.getuser()

# Check if destination directory exists, if not then create it
backup_path = Path(f"/home/{user}/.plasma-cfg-backup")
if not backup_path.exists():
    print(f"'/home/{user}/.plasma-cfg-backup' does not exist.  Creating it now.")
    try:
        backup_path.mkdir(exist_ok = True)
        print("Directory created.")
    except OSError as e:
        print(f"Error creating directory: {e}")

# Get list of plasma cfg filenames from .config directory
cfg_path = Path(f"/home/{user}/.config")
files = [file.name for file in cfg_path.iterdir() if file.is_file() and "plasma" in file.name]

# Copy config files to backup directory
for file in files:
    src = f"{str(cfg_path)}/{file}"
    shutil.copy(src, str(backup_path))

# Plasma backup readme content
readme_content = []

# Backup plasma 6.2 colors
colors_path = Path(f"/home/{user}/.local/share/color-schemes")
if colors_path.exists():
    colors_backup_path = Path(f"{str(backup_path)}/plasma/color-schemes")

    colors_backup_path.mkdir(parents = True, exist_ok = True)
    color_files = [file.name for file in colors_path.iterdir() if file.is_file()]
    for file in color_files:
        color_src = f"{str(colors_path)}/{file}"
        shutil.copy(color_src, str(colors_backup_path))

    readme_content.append("COLORS:\ncolor-schemes directory: /home/[user]/.local/share/color-schemes\nMove backed up color files to this directory on your machine.\n")

# Build readme file
if len(readme_content) > 0:
    readme_path = f"{str(backup_path)}/plasma/readme.txt"
    with open(readme_path, "w") as file:
        file.write("".join(readme_content))

print("Successfully backed up plasma config files.")
