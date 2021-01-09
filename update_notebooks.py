import os
import subprocess
import yaml

_root_nbsbasic = "./notebooks/engineering-basic/nbs"
_root_nbsanalysis = "./notebooks/data_analysis/nbs"
nbsbasic_root = "https://nbsbasic.herokuapp.com/notebooks"
nbsanalysis_root = "https://nbsanalysis.herokuapp.com/notebooks"



def search_data(url_root, path, module, extension):
    data_files = {}
    for root, dirs, files in os.walk(path + module, topdown=False):
        for name in files:
            if name.endswith(extension):
                data_files[name] = url_root + root.replace(path, "") + "/" + name
        for name in dirs:
            if name.endswith(extension):
                data_files[name] = url_root + root.replace(path, "") + "/" + name
    return data_files

def update_data():
    data = {"nbsbasic": {}, "nbsanalysis": {}}
    for j in range(1, 8):
        data["nbsbasic"]["module_" + str(j)] = search_data(nbsbasic_root, _root_nbsbasic, "/module_" + str(j), extension=".ipynb")
        data["nbsanalysis"]["module_" + str(j)] = search_data(nbsanalysis_root, _root_nbsanalysis, "/module_" + str(j), extension=".ipynb")


    with open("./server-admin" + "/database_notebooks.yml", "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
             
