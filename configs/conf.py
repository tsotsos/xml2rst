#START-XML2RST
# Configuration file from XML2RST.
#
# This file is totaly compatible with conf.py of Sphinx. In case you change code
# take care the imports we already import os, subprossess here.


import os
import subprocess

def yes_or_no(question):
    answer = input(question + "(y/n): ").lower().strip()
    print("")
    while not(answer == "y" or answer == "yes" or \
    answer == "n" or answer == "no"):
        print("Answer with a yes or no!")
        answer = input(question + "(y/n):").lower().strip()
        print("")
    if answer[0] == "y":
        return True
    else:
        return False

def simple_conf_parse ( cf ) :
    results = dict()
    if not os.path.isfile(cf):
        return False

    with open(cf,'r') as f:
        line = f.readline()
        while line:
            spl = line.split("=",2)
            if len(spl) == 2 :
                key = spl[0].rstrip('\n').strip()
                value = spl[1].rstrip('\n').strip()
                results.update({key:value})
            line = f.readline()
    return results

def find_file(filename):

    folder = os.getcwd()

    while folder != "/" and filename not in os.listdir(folder):
        folder = os.path.abspath(folder + "/../")

    filepath = os.path.join(folder,filename)
    if os.path.isfile(filepath):
        return filepath

    return False

def get_configs():

    version_data = dict()

    # first of all we need to identify VERSIONS file we trust only this to
    # find paths. Intially they are relative but we turn them into absolute
    # to ensure shpinx proper execution

    version_file = find_file("VERSIONS")
    # rootpath is nessessary to create paths
    rootpath = os.path.dirname(version_file)
    # rootpath = os.path.relpath(rootpath,os.getcwd())

    # find doxyfile
    doxyfile_file = find_file("Doxyfile")
    #doxyfile_file = os.path.relpath(doxyfile_file,os.getcwd())
    # parse doxyfile for output folder
    doxyfile_data = simple_conf_parse(doxyfile_file)
    doxyfile_dir  = os.path.dirname(doxyfile_file)
    if doxyfile_data["OUTPUT_DIRECTORY"] == ".":
        doxyfile_out_dir = os.path.abspath(doxyfile_dir)
    else:
        doxyfile_out_dir = os.path.relpath(
                                doxyfile_data["OUTPUT_DIRECTORY"],
                                doxyfile_dir)
        doxyfile_out_dir = os.path.abspath(doxyfile_out_dir)

    doxyfile_xml_dir = doxyfile_out_dir+"/"+doxyfile_data["XML_OUTPUT"]
    # parse version_file values to dict()
    version_data = simple_conf_parse(version_file)
    if not version_data:
        return False
    if version_data is None:
        return False

    # check for source path
    srcpath = rootpath+"/"+version_data["SRC"]
    srcpath = os.path.abspath(srcpath)
    if os.path.isdir(srcpath):
        version_data.update({"SRC":srcpath})
    else:
        return False

    # check for docs path
    docspath = rootpath+"/"+version_data["DOCS"]
    docspath = os.path.abspath(docspath)
    if os.path.isdir(srcpath):
        version_data.update({"DOCS":docspath})
    else:
        return False

    version_data.update({"DOXYFILE_XML":doxyfile_xml_dir})
    version_data.update({"ROOT":rootpath})
    version_data.update({"DOXYFILE":doxyfile_file})
    version_data.update({"READTHEDOCS":True})
    return version_data

config = get_configs()
if not config:
    print ("Error! Please check your VERSIONS file in root path")
    exit()

#Ask to run doxygen XML generation
if yes_or_no("Do you want to run doxygen XML generation?"):
    subprocess.call(["doxygen",config["DOXYFILE"]]
                    ,cwd=config["DOCS"]
                    ,stdout=subprocess.DEVNULL)
else:
    #if not os.path.isdir()
    print("ok we will continue...")

# generate sources
subprocess.call(['python',
                'generate.py',
                config["SRC"],
                os.getcwd(),
                config["EXCLUDED"]]
                )

#END-XML2RST

#START-BREATH
# PHP and BREATH Settings for Sphinx
extensions += ['sphinxcontrib.phpdomain']
extensions += ['breathe']

# Set up PHP syntax highlights
from sphinx.highlighting import lexers
from pygments.lexers.web import PhpLexer
lexers["php"] = PhpLexer(startinline=True, linenos=1)
lexers["php-annotations"] = PhpLexer(startinline=True, linenos=1)
primary_domain = "php"

#setup breath
breathe_projects = {config["PROJECT_NAME"]:config["DOXYFILE_XML"]}
if config["READTHEDOCS"] == True:
  import sphinx_rtd_theme
  html_theme = "sphinx_rtd_theme"
  html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
breathe_default_project = config["PROJECT_NAME"]
breathe_implementation_filename_extensions = ['.php']
#END-BREATH
