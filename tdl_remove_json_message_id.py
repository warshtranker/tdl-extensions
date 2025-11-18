import json
import os

def load_json_file(filename):
    """Load and return the JSON data from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filename}'.")
        return None

def save_json_file(filename, data):
    """Save JSON data to file"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"Data successfully saved to '{filename}'")
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def display_messages(messages):
    """Display all messages with their IDs"""
    if not messages:
        print("No messages found.")
        return
    
    print("\nCurrent messages:")
    print("-" * 50)
    for msg in messages:
        msg_id = msg.get('id', 'N/A')
        msg_type = msg.get('type', 'N/A')
        msg_date = msg.get('date', 'N/A')
        msg_from = msg.get('from', 'N/A')
        print(f"ID: {msg_id:3} | Type: {msg_type:8} | Date: {msg_date:19} | From: {msg_from}")

def remove_message_by_id(messages, target_id):
    """Remove a specific message by ID"""
    original_count = len(messages)
    messages[:] = [msg for msg in messages if msg.get('id') != target_id]
    
    removed_count = original_count - len(messages)
    if removed_count > 0:
        print(f"Removed {removed_count} message(s) with ID {target_id}")
    else:
        print(f"No message found with ID {target_id}")
    
    return removed_count > 0

def remove_multiple_messages_by_id(messages, id_string):
    """Remove multiple messages by IDs separated by commas"""
    try:
        # Split the input string by commas and convert to integers
        id_list = [int(id_str.strip()) for id_str in id_string.split(',')]
        
        original_count = len(messages)
        messages[:] = [msg for msg in messages if msg.get('id') not in id_list]
        
        removed_count = original_count - len(messages)
        if removed_count > 0:
            print(f"Removed {removed_count} message(s) with IDs: {', '.join(map(str, id_list))}")
        else:
            print(f"No messages found with the specified IDs")
        
        return removed_count > 0
    except ValueError:
        print("Error: Invalid input. Please enter numbers separated by commas (e.g., '10,78,45')")
        return False

def remove_all_before_id(messages, target_id):
    """Remove all messages before the specified ID"""
    # Find the index of the target ID
    target_index = -1
    for i, msg in enumerate(messages):
        if msg.get('id') == target_id:
            target_index = i
            break
    
    if target_index == -1:
        print(f"No message found with ID {target_id}")
        return False
    
    if target_index == 0:
        print("No messages to remove before the specified ID")
        return False
    
    removed_count = target_index
    messages[:] = messages[target_index:]
    print(f"Removed {removed_count} message(s) before ID {target_id}")
    return True

def remove_all_after_id(messages, target_id):
    """Remove all messages after the specified ID"""
    # Find the index of the target ID
    target_index = -1
    for i, msg in enumerate(messages):
        if msg.get('id') == target_id:
            target_index = i
            break
    
    if target_index == -1:
        print(f"No message found with ID {target_id}")
        return False
    
    if target_index == len(messages) - 1:
        print("No messages to remove after the specified ID")
        return False
    
    removed_count = len(messages) - target_index - 1
    messages[:] = messages[:target_index + 1]
    print(f"Removed {removed_count} message(s) after ID {target_id}")
    return True

def get_save_filename(default_filename):
    """Get filename from user or use default"""
    new_filename = input(f"Enter filename to save (or press Enter for '{default_filename}'): ").strip()
    if not new_filename:
        return default_filename
    # Add .json extension if not present
    if not new_filename.lower().endswith('.json'):
        new_filename += '.json'
    return new_filename

def main():
    filename = "duplicates.json"
    
    # Load JSON data
    data = load_json_file(filename)
    if data is None:
        return
    
    # Check if messages key exists
    if 'messages' not in data:
        print("Error: 'messages' key not found in JSON data")
        return
    
    messages = data['messages']
    
    while True:
        print("\n" + "="*50)
        print("JSON Message Editor")
        print("="*50)
        display_messages(messages)
        
        print("\nOptions:")
        print("1. Remove a specific message by ID")
        print("2. Remove multiple messages by IDs (comma-separated)")
        print("3. Remove all messages BEFORE a specific ID")
        print("4. Remove all messages AFTER a specific ID")
        print("5. Save changes and exit")
        print("6. Exit without saving")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            try:
                target_id = int(input("Enter the message ID to remove: "))
                remove_message_by_id(messages, target_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        
        elif choice == '2':
            id_input = input("Enter message IDs to remove (comma-separated, e.g., '10,78,45'): ").strip()
            if id_input:
                remove_multiple_messages_by_id(messages, id_input)
            else:
                print("No IDs entered.")
        
        elif choice == '3':
            try:
                target_id = int(input("Enter the message ID (remove all BEFORE this ID): "))
                remove_all_before_id(messages, target_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        
        elif choice == '4':
            try:
                target_id = int(input("Enter the message ID (remove all AFTER this ID): "))
                remove_all_after_id(messages, target_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        
        elif choice == '5':
            save_filename = get_save_filename(filename)
            if save_json_file(save_filename, data):
                print("Changes saved successfully!")
            break
        
        elif choice == '6':
            print("Exiting without saving.")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1-6.")

if __name__ == "__main__":
    main()