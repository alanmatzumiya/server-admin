import os
import subprocess
import yaml


repos = yaml.load(open('repositories.yml'), Loader=yaml.FullLoader)
containers = repos["containers"]
_root = "./containers/"
url_root = "https://github.com/alanmatzumiya"
branch = "/blob/main"


def search_data(path_target, extension):
    data_files = {}
    for root, dirs, files in os.walk(path_target, topdown=False):
        for name in files:
            if name.endswith(extension):
                data_files[name] = url_root+path_target.replace(_root, "/") + root.replace(path_target, branch) + "/" + name + "?raw=true"
        for name in dirs:
            if name.endswith(extension):
                data_files[name] = url_root+path_target.replace(_root, "/") + root.replace(path_target, branch) + "/" + name + "?raw=true"
    return data_files

def update_data():

    data = {}    
    for cont in list(containers.keys()):
        data[cont] = search_data(_root + cont,  tuple([".mp4", ".png", ".jpg", ".jpeg"]))

    with open("./server-admin" + "/database_containers.yml", "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)       
