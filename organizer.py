from pathlib import Path
import shutil
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# The folder to be organized.
target_directory = Path('cluttered_folder')

# Number of days after which a file is considered "old" and should be archived.
DAYS_TO_ARCHIVE = 30 

# Dictionary mapping file extensions to folder names.
FILE_CATEGORIES = {
    # Images
    'images': ['.jpg', '.jpeg', '.png', '.gif'],
    # Documents
    'Documents': ['.pdf', '.docx', '.txt'],
    # Archives
    'Archives': ['.zip', '.rar', '.7z'],
    # Code
    'Code': ['.py', '.js', '.html'],
}

# --- SETUP AND DIRECTORY CREATION ---

def setup_directories(target_directory):
  # Create all necessary destination folders
  all_folders = list(FILE_CATEGORIES.keys()) + ['Miscellaneous', 'Old_Files']
  for folder in all_folders:
    (target_directory/folder).mkdir(parents=True, exist_ok=True)

# --- MAIN ORGANIZATION LOGIC ---
def file_organization(target_directory):
  now = datetime.now()
  archive_threshold = now - timedelta(days=DAYS_TO_ARCHIVE)
  archive_folder_path = target_directory/'Old_Files'
  
  for source_path in target_directory.iterdir():
    filename  = source_path.name
    # Skip directories, process only files
    if source_path.is_dir():
      continue
    
    # --- 1. Check for old files first ---
    try:
      file_mod_time_stamp = source_path.stat().st_mtime
      file_mod_time = datetime.fromtimestamp(file_mod_time_stamp)
      
      if file_mod_time < archive_threshold:
        shutil.move(source_path, archive_folder_path/filename)
        print(f"Archived: {filename} -> Old_Files/")
        continue # Skip to the next file
    except Exception as e:
      print(f"Could not check age for {filename}. Error: {e}")
    
    # --- 2. If not old, sort by file type ---
    extension = source_path.suffix.lower()
    dest_folder = 'Miscellaneous'
    for folder, ext_list in FILE_CATEGORIES.items():
      if extension in ext_list:
        dest_folder = folder
        break
    destination_path = target_directory/dest_folder/filename
    shutil.move(source_path, destination_path)
    print(f"Moved: {filename} -> {dest_folder}/")

def main():
  print("--- Automated Portfolio Organizer ---")
  setup_directories(target_directory)
  print("Directory setup complete.")
  print("\nStarting file organization...")
  file_organization(target_directory)
  print("\n--- Organization complete! ---")

if __name__ == "__main__":
  main()