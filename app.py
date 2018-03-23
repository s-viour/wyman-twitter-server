import os
import json
from time import sleep
from Server import Server


def do_jobs():
    for file in os.listdir("jobs"):
        if file.endswith(".wyman"):
            Server(os.path.join("jobs/" + file)).start()


while True:
    sleep(int(json.loads(open("config.json", "r").read())["job_interval"]))
    do_jobs()
