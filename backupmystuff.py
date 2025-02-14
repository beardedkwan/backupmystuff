from pathlib import Path
import getpass
import shutil

# Get logged in user for directory paths
user = getpass.getuser()

'''
'''
'''
BACKUP PLASMA CONFIG FILES
'''
'''
'''

# Check if destination directory exists, if not then create it
mangohud_backup_path = Path(f"/home/{user}/.backups/plasma")
if not mangohud_backup_path.exists():
    print(f"'/home/{user}/.backups/plasma/' does not exist. Creating it now.")
    try:
        mangohud_backup_path.mkdir(parents = True, exist_ok = True)
    except OSError as e:
        print(f"Error creating directory: {e}")

# Get list of plasma cfg filenames from .config directory
cfg_path = Path(f"/home/{user}/.config")
files = [file.name for file in cfg_path.iterdir() if file.is_file() and "plasma" in file.name]

# Plasma backup readme content
readme_content = []

# Readme for .config files
readme_content.append(f"Config files in the main directory (.backups/plasma/) go in: /home/user/.config/\n")

# BACKUP .CONFIG FILES
for file in files:
    src = f"{str(cfg_path)}/{file}"
    shutil.copy(src, str(mangohud_backup_path))

# BACKUP PLASMA COLORS
colors_path = Path(f"/home/{user}/.local/share/color-schemes")
if colors_path.exists():
    colors_mangohud_backup_path = Path(f"{str(mangohud_backup_path)}/color-schemes")

    colors_mangohud_backup_path.mkdir(parents = True, exist_ok = True)
    color_files = [file.name for file in colors_path.iterdir() if file.is_file()]
    for file in color_files:
        color_src = f"{str(colors_path)}/{file}"
        shutil.copy(color_src, str(colors_mangohud_backup_path))

    readme_content.append("\nCOLORS:\ncolor-schemes directory: /home/user/.local/share/color-schemes\nMove backed up color files to this directory on your machine.\n")

# Build readme file
if len(readme_content) > 0:
    readme_path = f"{str(mangohud_backup_path)}/readme.txt"
    with open(readme_path, "w") as file:
        file.write("".join(readme_content))

print("Successfully backed up plasma config files.")

'''
'''
'''
BACKUP PS1 VARIABLE FOR KONSOLE
'''
'''
'''

ps1 = ""

with open(f"/home/{user}/.bashrc", 'r') as file:
    for line in file:
        # Strip whitespace and ignore comments
        line = line.strip()
        if line.startswith('#') or not line:
            continue

        # Check if the line sets PS1
        if line.startswith('PS1=') or line.startswith('export PS1='):
            # Extract the value after the first '='
            ps1 = line.split('=', 1)[1].strip("'")
            break

if len(ps1) > 0:
    # Create ps1 backup path
    ps1_backup_path = Path(f"/home/{user}/.backups")
    if not ps1_backup_path.exists():
        print(f"'/home/{user}/.backups/' does not exist. Creating it now.")
        try:
            ps1_backup_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory: {e}")

    # Create ps1 backup text file
    with open(f"{str(ps1_backup_path)}/ps1.txt", "w") as file:
        file.write(f"PS1:\n{ps1}\nThis variable is set in ~/.bashrc PS1='yourPS1'\n")

    print("Successfully backed up PS1 variable into ps1.txt.")

'''
'''
'''
BACKUP MANGOHUD CONFIG FILES
'''
'''
'''

# Check if destination directory exists, if not then create it
mangohud_backup_path = Path(f"/home/{user}/.backups/mangohud")
if not mangohud_backup_path.exists():
    print(f"'/home/{user}/.backups/mangohud/' does not exist. Creating it now.")
    try:
        mangohud_backup_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory: {e}")

# Get list of mangohud cfg filenames from ~/.config/MangoHud directory
mango_cfg_path = Path(f"/home/{user}/.config/MangoHud")
mango_files = [file.name for file in mango_cfg_path.iterdir() if file.is_file()]

# Backup config files
for file in mango_files:
    src = f"{str(mango_cfg_path)}/{file}"
    shutil.copy(src, str(mangohud_backup_path))

# Mangohud backup readme
if len(mango_files) > 0:
    with open(f"{str(mango_cfg_path)}/readme.txt", "w") as file:
        file.write(f"MangoHud config files go in: ~/.config/MangoHud/\n")

print("Successfully backed up MangoHud config files.")
