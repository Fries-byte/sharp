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
    current_section = None

    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        if line.endswith(": {"):
            current_section = line[:-3].strip().lower()
            continue
        
        elif line == "}":
            current_section = None
            continue
        
        elif current_section == "variables":
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().rstrip(',')
                data["variables"][key] = value
        
        elif current_section == "scripts":
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().rstrip(',')
                data["scripts"][key] = value

    return data

def run_script(script_name, shrp_data, args):
    variables = shrp_data.get("variables", {})
    scripts = shrp_data.get("scripts", {})

    if script_name not in scripts:
        print(f"Error: Script '{script_name}' not found.")
        return
    
    if args:
        variables["save"] = args[0]

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

    shrp_data = parse_shrp_file(shrp_file)

    if len(sys.argv) > 1:
        script_name = sys.argv[1]
        args = sys.argv[2:]
        run_script(script_name, shrp_data, args)
    else:
        print("Available scripts:")
        for script in shrp_data.get("scripts", {}):
            print(f"  - {script}")

if __name__ == "__main__":
    main()
