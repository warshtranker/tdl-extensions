# script versions 1.0

# ******** H O W T O ***********

# The script will allow you to check already downloaded files, get list of not downloaded files and list of all duplicate files with different sizes

# WARNING! The script will save only ONE file with the same name and size.

"""
1. Export channel or group history to result.json file via telegram client (select only files in export popup) or tdl
2. Set "path_to_downloads" to the path with files you already downloaded from the selected channel or group
3. set fn_filter function to your tdl filter if you used any for filenamse in "path_to_downloads"
3. this script will find all files with the same name and different sizes and save them to "duplicates.json"
4. then script will check "path_to_downloads" for downloaded files and save only unique and not downloaded files to "download.json"

Use "duplicates.json" and "download.json" to download files via tdl.
You can download all duplicate files with the following tdl command to the "duplicates" subfolder, add MessageId before file name to prevent files rewriting:
   tdl dl -f "duplicates.json" --skip-same -l 4 -t 8 -d ./duplicates --template --% "{{.MessageId}}_{{ replace .FileName `|` `_` `?` `_` `\"` `_` \"\n\" `_`}}"

Directory structurefor example:
   /my_group_downloads/
   |__files/
   |__duplicates/
   |__result.json
   |__duplicates.json
   |__download.json

"""

import os

# ********* C O N F I G *********

path_to_downloads = "files" # folder with downloaded files from group or channel, filenames must be the same as in TG channel or group
path_to_json = "" # blank - current path, where result.json is located and where to save duplicates.json and download.json

def fn_filter(fn):
  # for command:
  #    tdl dl -f "result.json" --template --% "{{ replace .FileName `|` `_` `?` `_` `\"` `_` \"\n\" `_`}}"
  # functon is:
  return fn.replace('?', '_').replace("\n" ,"_").replace("|", "_").replace('"', '_')

# ********** B E G I N **********
if not os.path.isfile(os.path.join(path_to_json, "result.json")):
    print("result.json doesn't exists.\nNow quit.")
    exit()

import json
from collections import defaultdict

def process_and_save_files():    
    # File paths
    input_file = "result.json"
    duplicates_file = "duplicates.json"
    not_exists_file = "download.json"
    
    # Read original file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Track files and messages - now including file_size for comparison
    file_tracker = defaultdict(list)
    all_file_messages = []
    
    # Process messages
    for message in data.get("messages", []):
        if "file_name" in message:
            file_name = message["file_name"]
            file_size = message.get("file_size")  # Get file_size if available
            
            if file_name:
                # Store both message and file_size for comparison
                file_tracker[file_name].append((message, file_size))
                all_file_messages.append((file_name, message, file_size))
    
    # Find TRUE duplicates - files with multiple file_name + file_size combinations
    duplicate_messages = []
    combination_tracker = defaultdict(list)
    
    # First, group all messages by file_name + file_size combination
    for file_name, message_size_pairs in file_tracker.items():
        for message, file_size in message_size_pairs:
            combination = (file_name, file_size)
            combination_tracker[combination].append(message)
    
    # Now identify which file_names have multiple unique combinations
    file_name_combinations = defaultdict(set)
    for (file_name, file_size), messages in combination_tracker.items():
        file_name_combinations[file_name].add(file_size)
    
    # Only keep files that have multiple unique file_name + file_size combinations
    true_duplicate_files = {
        file_name for file_name, sizes in file_name_combinations.items() 
        if len(sizes) > 1  # Only files with multiple different sizes
    }
    
    # Now collect one message from each combination of true duplicate files
    seen_combinations = set()
    for (file_name, file_size), messages in combination_tracker.items():
        if file_name in true_duplicate_files and len(messages) > 0:
            combination = (file_name, file_size)
            if combination not in seen_combinations:
                duplicate_messages.append(messages[0])  # Take first message
                seen_combinations.add(combination)
    
    # Find non-existent non-duplicate files
    non_existent_messages = []
    
    # Consider a file as duplicate if it appears multiple times with ANY size
    duplicate_files_any_size = {name for name, messages in file_tracker.items() if len(messages) > 1}
    
    for file_name, message, file_size in all_file_messages:
        # Only check files that are NOT duplicates (by name)
        if file_name not in duplicate_files_any_size:
            file_path = os.path.join(path_to_downloads , fn_filter(file_name))
            if not os.path.exists(file_path):
                non_existent_messages.append(message)
    
    # Save duplicates.json with only true duplicates (multiple sizes)
    duplicates_data = data.copy()
    duplicates_data["messages"] = duplicate_messages
    with open(duplicates_file, 'w', encoding='utf-8') as f:
        json.dump(duplicates_data, f, indent=2, ensure_ascii=False)
    
    # Save not_exists
    notexists_data = data.copy()
    notexists_data["messages"] = non_existent_messages
    with open(not_exists_file, 'w', encoding='utf-8') as f:
        json.dump(notexists_data, f, indent=2, ensure_ascii=False)
    
    # Print statistics
    total_files_by_name = sum(len(messages) for messages in file_tracker.values() if len(messages) > 1)
    true_duplicate_count = len(true_duplicate_files)
    
    print(f"Files with duplicate names: {len([x for x in file_tracker.values() if len(x) > 1])}")
    print(f"True duplicates (multiple sizes): {true_duplicate_count}")
    print(f"Saved {len(duplicate_messages)} unique duplicate messages to {duplicates_file}")
    print(f"Saved {len(non_existent_messages)} non-existent messages to {not_exists_file}")

# Run the processing
if __name__ == "__main__":
    process_and_save_files()
