import subprocess
import os


class VCSTools:

    def __init__(self, repos, path):
        self.path = path
        self.repos = repos

    def git_action(self, repo, data, action):
        if action == "clone":

            if repo != "all":
                sentence = "cd " + self.path + " && git clone " + self.repos[data][repo]
                print(sentence)
                os.system(sentence)
            elif repo == "all":
                for category in list(self.repos.keys()):
                    for rep in list(self.repos[category].values()):
                        sentence = "cd " + self.path + " && git clone " + rep
                        print(sentence)
                        os.system(sentence)
        else:
            if repo != "all":
                sentence_1 = "cd " + self.path + repo
                os.system(sentence_1 + " && git init")
                branch = subprocess.getoutput(sentence_1 + " && git branch").replace("* ", "")
                sentence_2 = " && git add . && git commit -m 'auto' && git push origin " + branch
                print(sentence_1 + sentence_2)
                os.system(sentence_1 + sentence_2)

            elif repo == "all":
                for category in list(self.repos.keys()):
                    for rep in list(self.repos[category].keys()):
                        sentence_1 = "cd " + self.path + rep
                        os.system(sentence_1 + " && git init")
                        branch = subprocess.getoutput(sentence_1 + " && git branch").replace("* ", "")
                        sentence_2 = " && git add . && git commit -m 'auto' && git push origin " + branch
                        print(sentence_1 + sentence_2)
                        os.system(sentence_1 + sentence_2)
