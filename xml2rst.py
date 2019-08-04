#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os


def check_not_empty(text):

    while True:
        value = input(text)
        if not value:
            print("Please enter a valid value")
            continue
        else:
            break
    return value


def check_dir(root_path, text):
    while True:
        if not root_path:
            realpath = input(text)
        else:
            path = input(text)
            realpath = os.path.join(root_path, path)

        if not os.path.isdir(realpath):
            print("Please enter a valid path")
            continue
        elif not realpath:
            print("Please enter a valid path")
            continue
        else:
            break
    return realpath

def wizzard ( ):
    vals = dict()
    version_file = "version"

    ROOTPATH = check_dir(False, "Enter the Project's root path: ")
    SRCPATH = check_dir( ROOTPATH, "Enter src path (relative to root path): ")
    DOCSPATH = check_dir( ROOTPATH, "Enter docs path (relative to root path): ")
    vals["PROJECT_NAME"] = check_not_empty("Project Name: ")
    vals["VERSION"] = check_not_empty("Release: ")
    vals["EXTVERSION"] = input("Extra version eg. -rc-1 (optional): ")
    vals["AUTHOR"] = check_not_empty("Author(s) :")
    vals["CREDITS"] = check_not_empty(
        "Initial Contributor (later you can add more):")

    version_file = os.path.join(ROOTPATH, version_file)

    if os.path.isfile(version_file):
        print("File " + version_file +
              " exists, please overview the file and remove it to continue")
        exit()

    with open(version_file, 'w') as data:
        for key, val in vals.items():
            data.write('%s=%s\n' % (key, val))

def main():
    wizzard()

if __name__ == '__main__':
    main()

