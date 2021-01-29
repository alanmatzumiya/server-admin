import os
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify
import server_runner
import pyGitHub
import data_management
import autobahn
import yaml
import shutil
import random

## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")


server = Flask(__name__)
server.config["SECRET"] = "circuitalminds"
server.config["API"] = "https://circuitflow.herokuapp.com"
server.config["REPOS_PATH"] = "../repositories/"
server.config["DATABASE_PATH"] = "./databases/"
server.config["REPOS"] = yaml.load(open(server.config["DATABASE_PATH"] + "repositories.yml"), Loader=yaml.FullLoader)

workers = {
    "server_runner": server_runner.LocalRun(),
    "data_management": data_management.DataUpdaters(server.config["REPOS"], server.config["REPOS_PATH"]),
    "BotDriver": autobahn.BotDriver(),
    "pyGitHub": pyGitHub.VCSTools(server.config["REPOS"], server.config["REPOS_PATH"])
    }

playlist = {
    "Top2020": "https://youtube.com/playlist?list=PLU1cYDntAmw3w3vtqMjVgQED_FzzlSFCh",
    "myHub": "https://youtube.com/playlist?list=PLU1cYDntAmw0aYr8KIS1doIaI46BUCMsB"
}


@server.route("/circuit_api")
def circuit_api():

    data = request.args.get("data")
    option = request.args.get("option")

    print(requests.get(
        server.config["API"] + "/" + option + "_data/" + data + "?token=" + server.config["SECRET"]).json()
          )

    return redirect(url_for("home"))


@server.route("/data_management")    
def data_management():

    data = request.args.get("data")
    workers["data_management"].all_update(data, server.config["DATABASE_PATH"])
    
    return redirect(url_for("home"))
    

@server.route("/git")
def git():

    repo = request.args.get("repo")
    data = request.args.get("data")
    action = request.args.get("action")
    workers["pyGitHub"].git_action(repo, data, action)
    
    return redirect(url_for("home"))


@server.route("/get_data")
def get_data():

    name = request.args.get("name")
    action = request.args.get("action")
    if action == "playlist":

        workers["BotDriver"].get_playlist(
            playlist[name], name, server.config["DATABASE_PATH"] + "YouTubePlayList/"
        )


    else:

        song = workers["BotDriver"].youtube_search(name)
        workers["BotDriver"].youtube_downloader(song["url"])
        print(song)
        for file in os.listdir("./"):
            if file.endswith("mkv") or file.endswith("mp4") or file.endswith("webm"):
                cont = "container_" + str(random.randint(1, 10))
                shutil.move(
                    "./" + file,
                    server.config["REPOS_PATH"] + cont + "/part_"
                    + str(random.randint(1, 10)) + "/" + file
                )
                workers["pyGitHub"].git_action(cont, "containers", "push")
                workers["data_management"].all_update("containers", server.config["DATABASE_PATH"])
    return redirect(url_for("home"))
    

@server.route('/')
def home():

    print(request.path)
    print(request.remote_addr)
    
    return render_template(
                               'index.html',
                               repos_user=server.config["REPOS"]["alanmatzumiya"],
                               repos_org=server.config["REPOS"]["CircuitalMinds"],
                               containers=server.config["REPOS"]["containers"],
                               notebooks=server.config["REPOS"]["notebooks"]
                           )


if __name__ == '__main__':
    server.run('127.0.0.1', '5000', debug=True)
