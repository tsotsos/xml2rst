#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re
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

def doxyfile_gen(vals,srcpath,docspath):
    doxyfile_file = docspath+"/Doxyfile"
    doxyfile_confs = {
            "PROJECT_NAME":"\""+vals["PROJECT_NAME"]+"\"",
            "PROJECT_NUMBER":vals["VERSION"]+vals["EXTVERSION"],
            "PROJECT_BRIEF":"\""+vals["DESC"]+"\"",
            "PROJECT_LOGO":"", # to be added
            "OUTPUT_DIRECTORY":".", #not defined for now
            "OUTPUT_LANGUAGE":"\"English\"",
            "INPUT":srcpath, #relative src path
            "EXCLUDE":" ", #should allow exclude paths
            "CREATE_SUBDIRS":"YES",
            "OPTIMIZE_OUTPUT_FOR_C":"YES", # should make user choose
            "EXTRACT_ALL":"YES",
            "EXTRACT_PRIVATE":"YES",
            "EXTRACT_PACKAGE":"YES",
            "EXTRACT_STATIC":"YES",
            "EXTRACT_LOCAL_METHODS":"YES",
            "EXTRACT_ANON_NSPACES":"YES",
            "CASE_SENSE_NAMES":"YES", #default is also YES
            "RECURSIVE":"YES",
            "SOURCE_BROWSER":"YES",
            "INLINE_SOURCES":"YES",
            "GENERATE_HTML":"NO",
            "GENERATE_LATEX":"NO",
            "GENERATE_XML":"YES",
            "HAVE_DOT":"YES",
            "CALL_GRAPH":"YES",
            "CALLER_GRAPH":"YES"
            }
    subprocess.call(["doxygen","-g","-s"],stdout=subprocess.DEVNULL)
    rekeys = "|".join(doxyfile_confs.keys())
    r = re.compile('((?:'+rekeys+'))\s+=\s+(.*)')
    f1 = open("Doxyfile",'r')
    f2 = open(doxyfile_file,'w')
    for line in f1:
        for key,val in doxyfile_confs.items():
            if key in line:
                line = re.sub(r, r"\1 = "+val+"\n", line, count=1)
        f2.write(line)
    f1.close()
    f2.close()
    os.remove("Doxyfile")
    return doxyfile_file

def sphinx_setup(vals,docspath):
    subprocess.Popen(["sphinx-quickstart",
                        "-p "+vals["PROJECT_NAME"],
                        "-a "+vals["AUTHOR"],
                        "-v "+vals["VERSION"],
                        "-r "vals["VERSION"]+vals["EXTVERSION"],
                        "--epub",
                        "--sep",
                        "-l English",
                        "--ext-autodoc",
                        "--ext-doctest",
                        "--ext-intersphinx",
                        "--ext-todo",
                        "--ext-coverage",
                        "--ext-imgmath",
                        "--ext-viewcode",
                        "--makefile",
                        "--no-batchfile",
                        "-t _templates"
                        ],cwd=docspath
                 )
    print("Please press enter to continue")

def sphinx_conf(version_file,docspath):
    conf_file = docspath+"/source/conf.py"
    with open(conf_file, "a") as f:
        f.write("\na = 1")

def wizzard ( ):
    vals = dict()
    version_file = "VERSIONS"
    # retrieve paths and normalize relative to docs path
    rootpath = check_dir(False, "Enter the Project's root path: ")
    srcpath = check_dir( rootpath, "Enter src path (relative to root path): ")
    docspath = check_dir( rootpath, "Enter docs path (relative to root path): ")
    rel_srcpath = os.path.relpath(srcpath,rootpath)
    version_file = os.path.join(rootpath, version_file)
    xml2rst_file = os.path.join(rootpath,docspath)
    xml2rst_file = os.path.join(xml2rst_file,"XML2RST")
    vals["PROJECT_NAME"] = check_not_empty("Project Name: ")
    vals["DESC"] = check_not_empty("Project description: ")
    vals["VERSION"] = check_not_empty("Release: ")
    vals["EXTVERSION"] = input("Extra version eg. -rc-1 (optional): ")
    vals["AUTHOR"] = check_not_empty("Author(s) :")
    vals["SRC"]= rel_srcpath
    vals["DOCS"] = os.path.relpath(docspath,rootpath)
    #generate doxyfile and keep the path
    doxyfile_file = doxyfile_gen(vals,rel_srcpath,docspath)
    vals["DOXYFILE"] = os.path.relpath(srcpath,doxyfile_file)

    if os.path.isfile(version_file):
        print("File " + version_file +
              " exists, please overview the file and remove it to continue")
        exit()

    with open(version_file, 'w') as data:
        for key, val in vals.items():
            data.write('%s=%s\n' % (key, val))
    data.close()
    #run doxygen Doxyfile to docs path
    #subprocess.Popen(["doxygen",docspath+"/Doxyfile"], cwd=docspath)
    sphinx_setup(vals,docspath)
    #sphinx_conf(version_file,docspath) #should check for versions file before

def main():
    wizzard()

if __name__ == '__main__':
    main()
