#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import string
import shutil
import subprocess

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

def doxyfilegen ( template, vals, srcpath, docspath ):
    vals = {
            "PROJECT_NAME":vals["PROJECT_NAME"],
            "PROJECT_NUMBER":vals["VERSION"]+vals["EXTVERSION"],
            "PROJECT_BRIEF":vals["DESC"],
            "PROJECT_LOGO":"", # to be added
            "OUTPUT_DIRECTORY":"output",
            "OUTPUT_LANGUAGE":"English",
            "SRC":srcpath,
            "EXCLUDE":""
            }
    #copy doxygen template to docs dir
    doxyfile = docspath+"/Doxyfile"
    shutil.copy2(template, doxyfile)

    f1 = open(template, "r")
    f2 = open(doxyfile, "w")
    for line in f1:
        for key,val in vals.items():
            line = line.replace("$$$"+key+"$$$", val)
            #print(line)
        f2.write(line)
    f1.close()
    f2.close()

def wizzard ( ):
    vals = dict()
    version_file = "VERSIONS"

    # retrieve paths and normalize relative to docs path
    rootpath = check_dir(False, "Enter the Project's root path: ")

    srcpath = check_dir( rootpath, "Enter src path (relative to root path): ")
    docspath = check_dir( rootpath, "Enter docs path (relative to root path): ")
    rel_srcpath = os.path.relpath(srcpath,docspath)
    vals["PROJECT_NAME"] = check_not_empty("Project Name: ")
    vals["DESC"] = check_not_empty("Project description: ")
    vals["VERSION"] = check_not_empty("Release: ")
    vals["EXTVERSION"] = input("Extra version eg. -rc-1 (optional): ")
    vals["AUTHOR"] = check_not_empty("Author(s) :")
    vals["CREDITS"] = check_not_empty(
        "Initial Contributor (later you can add more):")

    version_file = os.path.join(rootpath, version_file)
    xml2rst_file = os.path.join(rootpath,docspath)
    xml2rst_file = os.path.join(xml2rst_file,"XML2RST")

    if os.path.isfile(version_file):
        print("File " + version_file +
              " exists, please overview the file and remove it to continue")
        exit()

    with open(version_file, 'w') as data:
        for key, val in vals.items():
            data.write('%s=%s\n' % (key, val))
    data.close()

    with open(xml2rst_file, 'w') as data:
        data.write("SRC = " + rel_srcpath + "\n")
        data.write("docspath = " + docspath + "\n")
    data.close()
    #generate Doxyfile
    doxyfilegen("templates/Doxyfile.template",vals,rel_srcpath,docspath)
    #run doxygen Doxyfile to docs path
    subprocess.Popen(["doxygen",docspath+"/Doxyfile"], cwd=docspath)

def main():
    wizzard()

if __name__ == '__main__':
    main()

