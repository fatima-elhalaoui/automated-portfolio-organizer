# Automated Portfolio Organizer

A command-line utility written in Python to organize a directory's files based on their type and modification date.

## Features

- **Flexible:** Organizes any directory specified by the user via a command-line argument.
- **Intelligent Sorting:** Uses a hybrid approach to categorize files. High-priority file types (Documents, Code, Archives) are sorted by specific extensions for accuracy, while general types (Images, Video, Audio) are sorted by their MIME type for scalability.
- **Archiving:** Moves files older than a configurable number of days (default: 30) to a separate `Old_Files` directory.
- **Logging:** All operations are logged to both the console and a persistent `organizer.log` file, providing a timestamped record of every action.

## Requirements

- Python 3.6+
- No external libraries are required.

## Usage

1.  Clone this repository to your local machine.
2.  Navigate to the project directory in your terminal.

Execute the script, passing the path to the directory you wish to organize as an argument.

**Command:**
```bash
python organizer.py <path_to_directory>