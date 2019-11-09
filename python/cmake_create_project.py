#! /usr/bin/env python3
import argparse
import os

GIT_IGNORE="""
*~
*.layout
*.depend
/build*
/.idea/
/cmake-build-debug/

# Windows image file caches
Thumbs.db

# Folder config file
Desktop.ini

# Mac crap
.DS_Store
"""

GIT_ATTRIBUTES="""# Auto detect text files and perform LF normalization
* text eol=lf
install_vcpkg_dependencies.bat eol=crlf

*.ttf binary
*.png binary
*.gif binary
*.bmp binary
"""

INSTALL_VCPKG_DEPENDENCIES_BAT="""
@echo off
for /f "delims=" %%a in (vcpkg_dependencies) DO (
	vcpkg install %%a
)
"""

INSTALL_VCPKG_DEPENDENCIES_SH="""#!/bin/sh -e
while read -r dependency; do
	vcpkg install $dependency
done < vcpkg_dependencies
"""

CMAKE = """cmake_minimum_required(VERSION 3.11...3.14)
# 3.11 support for FetchContent
# 3.14 support for Visual Studio 2019

set(VCPKG_ROOT $ENV{VCPKG_ROOT})
if(DEFINED ENV{VCPKG_ROOT} AND NOT DEFINED CMAKE_TOOLCHAIN_FILE)
	set(CMAKE_TOOLCHAIN_FILE "${VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake"
		CACHE STRING ""
	)
	message(STATUS "Uses VCPKG CMAKE_TOOLCHAIN_FILE")
endif()

project($project_name
	DESCRIPTION
		"Description for the project"
	LANGUAGES
		CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(SOURCES	
	src/main.cpp
)

find_package(Threads REQUIRED)

set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT $project_name)

add_executable($project_name ${SOURCES})

target_link_libraries($project_name
	PRIVATE
		Threads::Threads
)
"""

CPP_MAIN="""#include <iostream>

int main() {
	std::cout << "Hello World!\\n";
	return 0;
}
"""

def create_file(full_filename: str, content: str, verbose=False, newline="\n"):
	file = open(full_filename, "w", newline=newline)
	file.write(content)
	file.close()
	if verbose:
		print("\t" + full_filename)

def create_files(project_name: str, cmake: str, use_project_path: bool, verbose=False):
	if use_project_path:
		project_path = os.getenv("GITHUB", ".")
		try:
			os.chdir(project_path)
			print("GITHUB=" + project_path)
		except:
			print("Aborting, GITHUB=" + project_path + " folder does not exist")

	try:
		os.mkdir(project_name)
	except OSError as e:
		print("Aborting, project folder failed to be created: " + project_name)
		if verbose:
			print(e)
		exit()
	
	if verbose:		
		print("Created files:")

	create_file(project_name + "/CMakelists.txt", cmake, verbose)
	os.mkdir(project_name + "/src")
	create_file(project_name + "/src/main.cpp", CPP_MAIN, verbose)

	create_file(project_name + "/.gitignore", GIT_IGNORE, verbose)
	create_file(project_name + "/.gitattributes", GIT_ATTRIBUTES, verbose)
	create_file(project_name + "/install_vcpkg_dependencies.bat", INSTALL_VCPKG_DEPENDENCIES_BAT, verbose, "\r\n")
	create_file(project_name + "/install_vcpkg_dependencies.sh", INSTALL_VCPKG_DEPENDENCIES_SH, verbose)
	create_file(project_name + "/vcpkg_dependencies", "\n", verbose)

def run(args):
	cmake_content = CMAKE.replace("$project_name", args.project_name)
	create_files(args.project_name, cmake_content, args.github, args.verbose)

def main():
	parser = argparse.ArgumentParser(description = "Create a cmake template for your project")	
	parser.add_argument("-p", "--project_name", help="name of the project (no spaces)", dest="project_name", required=True)
	parser.add_argument("-g", "--github", help="create project using GITHUB enviroment variable", dest="github", action="store_const", const=True)
	parser.add_argument("-v", "--verbose", help="verbose information", dest="verbose", action="store_const", const=True)
	parser.set_defaults(func=run)
	args=parser.parse_args()
	args.func(args)

if __name__=="__main__":
	main()
