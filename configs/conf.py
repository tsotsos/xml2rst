import os
from subprocess import call

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

def get_configs():
    # check for XML2RST conf file first
    xml2rst_file = "XML2RST"
    # try to add one folder up
    if not os.path.isfile(xml2rst_file):
        xml2rst_file = "../"+ xml2rst_file

    xml2rst = simple_conf_parse(xml2rst_file)
    if not xml2rst:
        return False

    # check for versions file
    version_file = xml2rst["VERSIONS"]

    # try to add one folder up
    if not os.path.isfile(version_file):
        version_file = "../"+ version_file

    version_data = simple_conf_parse(version_file)
    if not version_data:
        return False

    result = { **xml2rst,**version_data }
    if not result:
        return False
    if result is None:
        return False
    return result

configs = get_configs()
if not configs:
    print ("Error! Please check your configuration files XML2RST in doc path and VERSIONS in root path")
    exit()

# doxyfile is always at the same path with XML2RST conf so:
doxyfile = configs["XML2RST"].replace("XML2RST","Doxyfile")
pritn(doxyfile)

# doxygen generation
# call(['doxygen', 'Doxyfile'])

# generate sources

breathe_projects = { "myproject" : "xml/" }
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
  html_theme = 'default'
else:
  import sphinx_rtd_theme
  html_theme = "sphinx_rtd_theme"
  html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
breathe_default_project = "myproject"
