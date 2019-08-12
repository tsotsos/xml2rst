#  written by Jongkyu Kim (j.kim@fu-berlin.de)

import os
import sys
import shutil
from pprint import pprint

#should be updated or use pygments to detect language.
FILETYPES = ["c","cc","cxx","cpp","c++","java","ii","ixx","ipp","i++","inl",
            "idl","ddl","odl","h","hh","hxx","hpp","h++","cs","d","php","php4",
            "php5","phtml","inc","m","markdown","md","mm","dox","py","pyw",
            "f90","f95","f03","f08","f","for","tcl","vhd","vhdl","ucf","qsf",
            "js","jsx"]

def generate_index (src, out, temp, exclude):
    """ Generates index.rst from source code """
    contents = []
    contents_tmp = ""

    for name in os.listdir(src):
        if os.path.isdir(os.path.join(src,name)) == True:
            if name not in exclude:
                contents.append(name)

    contents = sorted(contents)
    #read temp file
    with open(temp,"r") as ftmp:
        contents_tmp = ftmp.read()

    #write index.rst
    with open("index.rst", "w") as idx:
        idx.write(contents_tmp)
        idx.write(".. toctree::\n")
        idx.write("   :titlesonly:\n")
        idx.write("   :maxdepth: 1\n")
        idx.write("   :hidden:\n")
        idx.write("   :caption: Contents:\n\n")
        for name in contents :
            idx.write("   %s\n" % (name))
    return True

def generate_local_index (src,out,subfolders,files):
    """ Generates local index file for each directory """
    basename = os.path.basename(out)
    # title
    title = basename[0].upper() + basename[1:] + "\n"
    title += "=" * len(basename) + "\n\n"

    # todo add support for readme

    # toctree
    toctree = ".. toctree::\n"
    toctree +="   :caption: Contents:\n"
    toctree +="   :titlesonly:\n"
    toctree +="   :maxdepth: 2\n"
    toctree +="   :hidden:\n\n"

    # contents - subfolders
    for subfolder in subfolders:
        toctree += "   %s\n" % os.path.join(basename,subfolder)

    # contents - files
    for filename in files:
        filenoext = os.path.splitext(filename)[0]
        toctree += "   %s\n" % os.path.join(basename,filenoext)
        generate_local_files(src,out,filename)


    with open(out + ".rst","w") as f1:
        f1.write(title)
        f1.write(toctree)

def generate_local_files (src,out,file):
    """ Generates rst for each file """
    filenoext = os.path.splitext(file)[0]
    with open(os.path.join(out,filenoext+".rst"), "w") as f1:
        f1.write(filenoext[0].upper() + filenoext[1:]+"\n")
        f1.write("=" * len(filenoext) + "\n\n")
        f1.write(".. doxygenfile:: %s\n" % os.path.join(src,file))
        f1.write("   :project: Greeka Community API\n\n")

def generate_tree_walk (src,out,excludes):
    """ Recursively parse all files and folders, then generates
        indexes and dir stracture."""
    for root, dirs, files in os.walk(src):
        current_files = []
        path = root.split(os.sep)
        dirs[:] = [d for d in dirs if d not in excludes]
        if root == src or root in excludes or root.startswith("."):
            continue
        rel_root = os.path.join(out,os.path.relpath(root,src))
        if os.path.exists(rel_root):
            shutil.rmtree(rel_root)
        os.makedirs(rel_root)

        for filename in files:
            ext = filename.split(".")[-1]
            if filename in excludes and ext not in FILETYPES:
                continue
            if filename.startswith("."):
                continue
            current_files.append(filename)
        generate_local_index(root,rel_root,dirs,current_files)

SRC = sys.argv[1]
BUILD = sys.argv[2]
EXCLUDE = sys.argv[3]
EXCLUDE = EXCLUDE.split(",")
TEMP = "_index_tmp"

if not os.path.isfile(os.path.join(os.getcwd(),TEMP)):
    print ("Cannot find "+TEMP+" template file")
    exit()

generate_index(SRC,BUILD,TEMP,EXCLUDE)
generate_tree_walk(SRC,BUILD,EXCLUDE)
