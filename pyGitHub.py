import os
import subprocess
import yaml


repos = yaml.load(open('./databases/repositories.yml'), Loader=yaml.FullLoader)
root_path = "./repositories"

class pyGitHub:    

    def clone(repo_data):
        for category in list(repo_data.keys()):
            for repo in list(repo_data[category].values()):
                os.system("cd " + root_path + " && git clone " + repo)

    def push(repo_data):
        for category in list(repo_data.keys()):
            for repo_name in list(repo_data[category].keys()):
                os.system("cd " + root_path + "/" + repo_name + " && git init")
                branch = subprocess.getoutput("cd " + root_path + "/" + repo_name + " && git branch").replace("* ", "")
                print("cd " + root_path + "/" + repo_name + " && git init && git add . && git commit -m 'auto' && git push origin " + branch)
                #os.system("cd " + root_path + "/" + repo_name + " && git init && git add . && git commit -m 'auto' && git push origin main")            

class data_uploaders:
    repo_datas = {"containers": repos["containers"], "notebooks": repos["notebooks"] }
	containers = repos["containers"]
	_root = "./containers/"
	url_root = "https://github.com/alanmatzumiya"
	branch = "/blob/main"
    
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

	def update_data(fmt="yml"):

		data = {}    
		for cont in list(containers.keys()):
		    data[cont] = search_data(_root + cont,  tuple([".mp4", ".png", ".jpg", ".jpeg"]))

		if fmt == "json":
		    with open("./server-admin" + "/database_containers.json", "w") as outfile:
		        json_file = json.dumps(data, indent=4, sort_keys=True)
		        outfile.write(json_file)
		        outfile.close()
		else:            
		    with open("./server-admin" + "/database_containers.yml", "w") as outfile:
		        yaml.dump(data, outfile, default_flow_style=False)  
