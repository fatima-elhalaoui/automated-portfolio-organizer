import argparse
import logging
import mimetypes
from pathlib import Path
import shutil
from datetime import datetime, timedelta

# --- Configuration Constants ---
DAYS_TO_ARCHIVE = 30 

# DICTIONARY 1: High-priority, specific extensions for precise categorization.
EXTENSION_CATEGORIES = {
  'Code': ['.py', '.js', '.html', '.css'],
  'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
  'Documents': ['.pdf', '.docx', 'doc', '.txt', '.odt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx']
}

# DICTIONARY 2: Low-priority, general MIME types for broad categorization.
MIME_CATEGORIES = {
  'Images': 'image',
  'Video': 'video',
  'Audio': 'audio',
}

def setup_directories(target_directory: Path):
    """Creates all necessary destination folders before processing any files."""
    all_folders = list(EXTENSION_CATEGORIES.keys()) + list(MIME_CATEGORIES.keys()) + ['Miscellaneous', 'Old_Files']
    for folder in all_folders:
        (target_directory / folder).mkdir(parents=True, exist_ok=True)

def file_organization(target_directory: Path, logger):
    """
    Organizes files in the target directory by archiving old files and sorting
    the rest into categorized folders based on a hybrid extension/MIME type approach.
    """
    now = datetime.now()
    archive_threshold = now - timedelta(days=DAYS_TO_ARCHIVE)
    archive_folder_path = target_directory / 'Old_Files'
  
    for source_path in target_directory.iterdir():
        # Skip directories, process only files
        if not source_path.is_file():
            continue
            
        filename = source_path.name
        
        # Archive files older than the specified threshold.
        try:
            file_mod_time = datetime.fromtimestamp(source_path.stat().st_mtime)
            if file_mod_time < archive_threshold:
                shutil.move(str(source_path), archive_folder_path / filename)
                logger.info(f'Archived: {filename} -> Old_Files/')
                continue
        except Exception as e:
            logger.error(f'Could not check age for {filename}. Error: {e}')
    
        # Sort remaining files using a two-phase hybrid approach for precision and scalability.
        extension = source_path.suffix.lower()
        dest_folder = 'Miscellaneous'
        found_category = False

        # Phase 1: Check for high-priority, specific extensions first.
        for category, extensions in EXTENSION_CATEGORIES.items():
            if extension in extensions:
                dest_folder = category
                found_category = True
                break
        
        # Phase 2: If no specific match was found, fall back to general MIME types.
        if not found_category:
            mime_type, _ = mimetypes.guess_type(filename)
            if mime_type is not None:
                main_type = mime_type.split('/')[0]
                for category, targeted_main_type in MIME_CATEGORIES.items():
                    if targeted_main_type == main_type:
                        dest_folder = category
                        break

        destination_path = target_directory / dest_folder / filename
        shutil.move(str(source_path), str(destination_path))
        logger.info(f'Moved: {filename} -> {dest_folder}/')

def main():
    """Main entry point for the script."""
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Organizes files in a target directory by type and age.")
    parser.add_argument("target_directory", type=Path, help="The path to the directory to be organized.")
    args = parser.parse_args()
    target_dir = args.target_directory

    # --- Logger Setup ---
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Setup file handler to save logs to a file
    file_handler = logging.FileHandler('organizer.log')
    file_handler.setFormatter(formatter)
    
    # Setup console handler to show logs on the screen
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # --- Application Logic ---
    logger.info('--- Automated Portfolio Organizer ---')
    logger.info(f'Organizing directory: {target_dir}')
    
    setup_directories(target_dir)
    logger.info('Directory setup complete.')
    
    logger.info('Starting file organization.')
    file_organization(target_dir, logger)
    
    logger.info('--- Organization complete! ---')

if __name__ == '__main__':
  main()