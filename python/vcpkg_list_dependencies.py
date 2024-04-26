#! /usr/bin/env python3
import os
import platform
import subprocess
import json
import argparse

def get_vcpkg_executable() -> str:
    if platform == "win32":
        return "vcpkg.exe"
    else:
        return "vcpkg"

def vcpkg_list_deps(vcpkg_json_path: str, verbose: bool):
    if os.path.isdir(vcpkg_json_path):
        path = os.path.join(vcpkg_json_path, 'vcpkg.json')
    elif vcpkg_json_path.endswith('vcpkg.json'):
        path = vcpkg_json_path
    else:
        print(f"Error: Invalid path {vcpkg_json_path}")
        return

    # Check if the vcpkg.json file exists
    if not os.path.isfile(path):
        print(f"Error: vcpkg.json file not found at {path}")
        return

    # Read the vcpkg.json file
    file = open(path, "r")
    if not file:
        print(f"Error: Could not open file at {path}")
        return
    data = json.loads(file.read())
    
    vcpkg = os.environ['VCPKG_ROOT']
    if vcpkg == None:
        print("Error: VCPKG_ROOT environment variable not set")
        return
    
    vcpkg = os.path.join(vcpkg, get_vcpkg_executable())
    
    # Run the bash command
    for dep in data['dependencies']:
        bash_command = f"{vcpkg} depend-info {dep} --format=tree 2>&1"
        if verbose:
            print(f"Running command: {bash_command}")
        subprocess.run(bash_command, shell=True)

def run(args):
    vcpkg_list_deps(args.vcpkg_json_path, args.verbose)

def main():
    parser = argparse.ArgumentParser(description = "List all dependencies in the vcpkg.json (uses 'vcpkg depend-info' command)")
    parser.add_argument("vcpkg_json_path", help="path to the vcpkg.json file or folder containing the vcpkg.json file")
    parser.add_argument("-v", "--verbose", help="print verbose output", dest="verbose", action="store_const", const=True)
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

if __name__=="__main__":
    main()
