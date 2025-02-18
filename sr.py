import os
import json
import re

def parse_shrp_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    # Parse the content into a dictionary
    data = {
        "scripts": {},
        "": "Compiled to json with Sharp"
    }
    current_section = None
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        # Check for section headers
        if line.endswith(':'):
            current_section = line[:-1].strip()
            continue
        
        # Parse scripts
        elif current_section == "scripts":
            if ":" in line:
                key, value = line.split(":", 1)
                data["scripts"][key.strip()] = value.strip()
    
    return data

def compile_to_json(shrp_data, output_path):
    with open(output_path, 'w') as json_file:
        json.dump(shrp_data, json_file, indent=4)

def main():
    # Find all .shrp files in the current directory
    for file_name in os.listdir('.'):
        if file_name.endswith('.shrp'):
            # Parse the .shrp file
            shrp_data = parse_shrp_file(file_name)
            
            # Create the output .json file name
            json_file_name = file_name.replace('.shrp', '.json')
            
            # Compile the .shrp data into a .json file
            compile_to_json(shrp_data, json_file_name)
            
            print(f"Compiled {file_name} to {json_file_name}")

if __name__ == "__main__":
    main()
