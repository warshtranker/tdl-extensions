# tdl-extensions
Telegram Downloader extensions


duplicate_sorter.py - A Python script that processes Telegram channel/group messages from result.json and organizes files for efficient downloading. The script performs the following operations:
1. Identifies Duplicate Files: Analyzes messages to find files with identical names but different sizes, saving them to duplicates.json
2. Creates Download List: Generates download.json containing only unique files that don't exist in your download path
4. The resulting download.json and duplicates.json can be used with tdl (https://github.com/iyear/tdl) to download all duplicates and new files efficiently
5. Workflow: result.json → (duplicate detection + local file check) → duplicates.json + download.json → tdl download
6. This approach ensures you only download missing files while maintaining a record of all duplicates found in the Telegram export data.
