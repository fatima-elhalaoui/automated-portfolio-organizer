# Automated Portfolio Organizer

A Python script that organizes files in a directory by their type and archives files older than a specified number of days. This is a foundational project I built to practice core Python concepts.

## Features

- Scans a target directory for all files.
- Moves files into categorized subdirectories (e.g., Images, Documents, Code) based on their extension.
- Identifies files older than a configurable number of days (default: 30) and moves them to an `Old_Files` archive.
- Creates all necessary folders automatically if they don't exist.

## How to Use

1.  Ensure you have Python 3 installed.
2.  Place the `organizer.py` script in a folder.
3.  Create a subfolder inside that folder named `cluttered_folder`.
4.  Place the files you want to organize inside `cluttered_folder`.
5.  Run the script from your terminal: `python organizer.py`

## Concepts Practiced

- **File System Interaction:** `os` and `shutil` modules.
- **Date & Time Manipulation:** `datetime` module for checking file ages.
- **Data Structures:** Using dictionaries to map file types to folders.
- **Conditional Logic & Error Handling.**