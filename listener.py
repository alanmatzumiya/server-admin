import requests
from time import sleep

url_workers = "https://circuitflow.herokuapp.com/workers"
host = "http://127.0.0.1:5000"
workers_root = {
    "server_runner": "/runner",
    "data_management": "/data_management",
    "BotDriver": "/get_data",
    "pyGitHub": "/git"
    }


def get_info(url):

    return requests.get(url).json()


while True:

    info_workers = get_info(url_workers + "?option=view")
    workers = list(info_workers.keys())
    status = len(workers)

    if status > 1:
        print(info_workers)
        for worker_id in workers[1:]:
            number = worker_id
            worker = info_workers[worker_id]["worker"]
            job = info_workers[worker_id]["job"]
            argument = info_workers[worker_id]["argument"]
            requests.get(host + workers_root[worker] + "?option=" + job + "&name=" + argument)
            print("worker " + number + " finished")
            print(requests.get(url_workers + "?option=delete" + "&worker=" + worker).json())
    sleep(5)
