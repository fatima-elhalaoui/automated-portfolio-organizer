import logging
import mimetypes
from pathlib import Path
import shutil
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# The folder to be organized.
target_directory = Path('cluttered_folder')

# Number of days after which a file is considered 'old' and should be archived.
DAYS_TO_ARCHIVE = 30 

# Dictionary mapping folders to mimetypes.
# DICTIONARY 1: High-priority, specific extensions
EXTENSION_CATEGORIES = {
  'Code': ['.py', '.js', '.html', '.css'],
  'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
  'Documents': ['.pdf', '.docx', 'doc', '.txt', '.odt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx']
}

# DICTIONARY 2: Low-priority, general MIME types (our fallback)
MIME_CATEGORIES = {
  'Images': 'image',
  'Video': 'video',
  'Audio': 'audio',
}

# --- SETUP AND DIRECTORY CREATION ---
def setup_directories(target_directory: Path):
  # Create all necessary destination folders
  all_folders = list(EXTENSION_CATEGORIES.keys()) + list(MIME_CATEGORIES.keys()) + ['Miscellaneous', 'Old_Files']
  for folder in all_folders:
    (target_directory / folder).mkdir(parents=True, exist_ok=True)

# --- MAIN ORGANIZATION LOGIC ---
def file_organization(target_directory: Path, logger):
  now = datetime.now()
  archive_threshold = now - timedelta(days=DAYS_TO_ARCHIVE)
  archive_folder_path = target_directory / 'Old_Files'
  
  for source_path in target_directory.iterdir():
    if not source_path.is_file():
      continue
      
    filename = source_path.name
    
    # --- 1. Check for old files first ---
    try:
      file_mod_time_stamp = source_path.stat().st_mtime
      file_mod_time = datetime.fromtimestamp(file_mod_time_stamp)
      
      if file_mod_time < archive_threshold:
        shutil.move(str(source_path), archive_folder_path / filename)
        logger.info(f'Archived: {filename} -> Old_Files/')
        continue
    except Exception as e:
      logger.error(f'Could not check age for {filename}. Error: {e}')
    
    # --- 2. If not old, sort by file type ---
    extension = source_path.suffix.lower()
    dest_folder = 'Miscellaneous'
    found_in_phase_one = False
    for folder, extensions in EXTENSION_CATEGORIES.items():
      if extension in extensions:
        dest_folder = folder
        found_in_phase_one = True
        break
    if not found_in_phase_one:
      mime_type, _ = mimetypes.guess_type(filename)
      if mime_type is not None:
        main_type = mime_type.split('/')[0]
        for folder, targeted_main_type in MIME_CATEGORIES.items():
          if targeted_main_type == main_type:
            dest_folder = folder
            break
    destination_path = target_directory / dest_folder / filename
    shutil.move(str(source_path), str(destination_path))
    logger.info(f'Moved: {filename} -> {dest_folder}/')

def main():
  # 1. Create a logger object
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.INFO)
  
  # 2. Create a formatter to define the message format
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  
  # 3. Create a handler to write logs to a file
  file_handler = logging.FileHandler('organizer.log')
  file_handler.setFormatter(formatter)
  
  # 4. Create a handler to show logs on the console
  console_handler = logging.StreamHandler()
  console_handler.setFormatter(formatter)
  
  # 5. Add both handlers to the logger
  logger.addHandler(file_handler)
  logger.addHandler(console_handler)
  logger.info('--- Automated Portfolio Organizer ---')
  setup_directories(target_directory)
  logger.info('Directory setup complete.')
  logger.info('Starting file organization.')
  file_organization(target_directory, logger)
  logger.info('--- Organization complete! ---')

if __name__ == '__main__':
  main()