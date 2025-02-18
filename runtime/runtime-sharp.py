import os
import json
import re
import subprocess
import sys

def parse_shrp_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    data = {
        "scripts": {},
        "variables": {},
        "": "Compiled to json with Sharp"
    }
    script_type = "compiled"
    current_section = None
    inside_block = False
    temp_dict = {}

    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("type:") and not inside_block:
            script_type = line.split(":", 1)[1].strip().strip('"')
            continue

        if line.endswith(": {"):
            current_section = line[:-3].strip().lower()
            inside_block = True
            temp_dict = {}
            continue
        
        elif line == "}":
            inside_block = False
            if current_section and temp_dict:
                data[current_section] = temp_dict
            current_section = None
            continue
        
        elif inside_block and current_section == "scripts":
            if ":" in line:
                key, value = line.split(":", 1)
                temp_dict[key.strip()] = value.strip().rstrip(',')

        elif inside_block and current_section == "variables":
            if "=" in line:
                key, value = line.split("=", 1)
                temp_dict[key.strip()] = value.strip().rstrip(',')

    return data, script_type

def compile_to_json(shrp_data, output_path):
    with open(output_path, 'w') as json_file:
        json.dump(shrp_data, json_file, indent=4)

def run_script(script_name, shrp_data):
    variables = shrp_data.get("variables", {})
    scripts = shrp_data.get("scripts", {})

    if script_name not in scripts:
        print(f"Error: Script '{script_name}' not found.")
        return
    
    command = scripts[script_name]

    for var, value in variables.items():
        command = command.replace(f"${var}", value)
    
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script '{script_name}': {e}")

def main():
    shrp_file = None
    for file_name in os.listdir('.'):
        if file_name.endswith('.shrp'):
            shrp_file = file_name
            break
    
    if not shrp_file:
        print("No .shrp file found.")
        return

    shrp_data, script_type = parse_shrp_file(shrp_file)

    if script_type == "direct":
        if len(sys.argv) > 1:
            script_name = " ".join(sys.argv[1:])
            run_script(script_name, shrp_data)
        else:
            print("Available scripts:")
            for script in shrp_data.get("scripts", {}):
                print(f"  - {script}")
    else:
        json_file_name = shrp_file.replace('.shrp', '.json')
        compile_to_json(shrp_data, json_file_name)
        print(f"Compiled {shrp_file} to {json_file_name}")

if __name__ == "__main__":
    main()
