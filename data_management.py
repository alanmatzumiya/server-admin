import os
import yaml
import json


class DataUpdaters:

    def __init__(self, repos, local_path):
        self.repos = repos
        self.local_path = local_path
        self.url_root = "https://github.com/alanmatzumiya/"

        self.data_containers = {
                "notebooks": {
                    "repos": list(repos["notebooks"].keys()),
                    "url": "https://jupyternbs.herokuapp.com/notebooks/",
                    "sub_url": "",
                    "url_extend": "",
                    "extension": "ipynb"
                },
                "containers": {
                    "repos": list(repos["containers"].keys()),
                    "url": "https://github.com/alanmatzumiya/",
                    "sub_url": "/blob/main",
                    "url_extend": "?raw=true",
                    "extension": tuple(["mkv", "webm", "mp4", "png", "jpeg", "jpg"])
                    }
                }

    def all_update(self, data, path_output):

        url = self.data_containers[data]["url"]
        sub_url = self.data_containers[data]["sub_url"]
        url_extend = self.data_containers[data]["url_extend"]
        extension = self.data_containers[data]["extension"]

        for repo in list(self.data_containers[data]["repos"]):
            file_data = self.data_search(url, sub_url, url_extend, self.local_path, repo, extension)
            print(file_data)
            if file_data != {}:
                self.save_data(file_data, path_output + repo)

    @staticmethod
    def data_search(url, sub_url, url_extend, root, path, extension):
        data = {}

        for sub_path, dirs, files in os.walk(root + path, topdown=False):
            for name in files:
                if name.endswith(extension):
                    data[name] = url + sub_path.replace(root + path, path + sub_url) + "/" + name + url_extend
            for name in dirs:
                if name.endswith(extension):
                    data[name] = url + sub_path.replace(root + path, path + sub_url) + "/" + name + url_extend
        return data

    @staticmethod
    def save_data(file_data, path_output, format_output="yml"):

        if format_output == "json":
            with open(path_output + ".json", "w") as outfile:
                json_file = json.dumps(file_data, indent=4, sort_keys=True)
                outfile.write(json_file)
                outfile.close()
        else:
            with open(path_output + ".yml", "w") as outfile:
                yaml.dump(file_data, outfile, default_flow_style=False)
