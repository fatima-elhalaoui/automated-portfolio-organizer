import os
import shutil
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# The folder to be organized.
target_directory = "cluttered_folder"

# Number of days after which a file is considered "old" and should be archived.
DAYS_TO_ARCHIVE = 30 

# Dictionary mapping file extensions to folder names.
FILE_CATEGORIES = {
    # Images
    '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images',
    # Documents
    '.pdf': 'Documents', '.docx': 'Documents', '.txt': 'Documents',
    # Archives
    '.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives',
    # Code
    '.py': 'Code', '.js': 'Code', '.html': 'Code',
}

# --- SETUP AND DIRECTORY CREATION ---
print("--- Automated Portfolio Organizer ---")

# Create all necessary destination folders
all_folders = list(set(FILE_CATEGORIES.values())) + ['Miscellaneous', 'Old_Files']
for folder in all_folders:
    os.makedirs(os.path.join(target_directory, folder), exist_ok=True)
print("Directory setup complete.")

# --- MAIN ORGANIZATION LOGIC ---
print("\nStarting file organization...")
now = datetime.now()
archive_threshold = now - timedelta(days=DAYS_TO_ARCHIVE)
archive_folder_path = os.path.join(target_directory, 'Old_Files')

for filename in os.listdir(target_directory):
    source_path = os.path.join(target_directory, filename)

    # Skip directories, process only files
    if not os.path.isfile(source_path):
        continue

    # --- 1. Check for old files first ---
    try:
        file_mod_time_stamp = os.path.getmtime(source_path)
        file_mod_time = datetime.fromtimestamp(file_mod_time_stamp)

        if file_mod_time < archive_threshold:
            shutil.move(source_path, os.path.join(archive_folder_path, filename))
            print(f"Archived: {filename} -> Old_Files/")
            continue # Skip to the next file
    except Exception as e:
        print(f"Could not check age for {filename}. Error: {e}")

    # --- 2. If not old, sort by file type ---
    extension = os.path.splitext(filename)[1].lower()
    dest_folder = FILE_CATEGORIES.get(extension, 'Miscellaneous')
    destination_path = os.path.join(target_directory, dest_folder, filename)
    
    shutil.move(source_path, destination_path)
    print(f"Moved: {filename} -> {dest_folder}/")

print("\n--- Organization complete! ---")