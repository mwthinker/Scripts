#! /usr/bin/env python3
import os
import platform
import subprocess
import sys
import json

def get_vcpkg_executable():
  if platform == "win32":
    return "vcpkg.exe"
  else:
    return "vcpkg"

def vcpkg_list_deps(vcpkg_json_path):
  path = os.path.join(vcpkg_json_path, 'vcpkg.json')

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
    bash_command = f"{vcpkg} depend-info {dep} --format=tree"
    #print(f"Running command: {bash_command}")
    bash_command = f"{vcpkg} depend-info {dep} --format=tree 2>&1"
    subprocess.run(bash_command, shell=True)

def print_usage():
  print("Usage: python vcpkg_list_dependencies.py <path-to-vcpkg.json>")
  print("List all dependencies in the vcpkg.json (uses 'vcpkg depend-info' command)")
  print()

def main():
  if len(sys.argv) < 2:
    print_usage()
    return

  vcpkg_json_path = sys.argv[1]
  vcpkg_list_deps(vcpkg_json_path)

if __name__=="__main__": 
    main() 
