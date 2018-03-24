import requests
import json
from time import sleep
import threading
from Watcher import Watcher
from Poster import Poster

running_jobs = []


def is_valid_user(username):
    try:
        user_page = requests.get("https://twitter.com/" + username)
    except requests.RequestException:
        return False
    if user_page.status_code != 200:
        return False
    return True


def is_valid_web_hook(hook):
    hook_post = None
    try:
        hook_post = requests.head(hook)
    except requests.RequestException:
        return False
    if hook_post.status_code != 200:
        return False
    return True


class Server:
    def __init__(self, wyman_file):
        self.file_path = wyman_file
        self.watcher_obj = None
        self.poster_obj = None
        self.twitter_user = None
        self.web_hook = None
        self.text_enabled = True
        self.images_enabled = True
        # default is 10 minutes (600 seconds)
        self.check_delay = 600

        with open(self.file_path, "r") as opened:
            try:
                self.config = json.loads(opened.read())
            except json.JSONDecodeError:
                print("Invalid configuration file [{}]!", self.file_path)
                return

        if is_valid_user(self.config["twitter_handle"]):
            self.twitter_user = self.config["twitter_handle"]
        if is_valid_web_hook(self.config["webhook"]):
            self.web_hook = self.config["webhook"]

        self.watcher_obj = Watcher(self.twitter_user)
        self.poster_obj = Poster(self.watcher_obj, self.web_hook)

        if str(self.config["text_enabled"]).lower() == "false":
            self.poster_obj.disable_text()
        if str(self.config["images_enabled"]).lower() == "false":
            self.poster_obj.disable_images()
        if str(self.config["links_enabled"]).lower() == "false":
            self.poster_obj.disable_links()

        try:
            self.check_delay = int(self.config["check_delay"])
        except ValueError:
            print("check_delay is not a number!\ndefaulting to 10 minute delay.")

    def start(self):
        if self.config in running_jobs:
            print("job for {} already running. skipping...".format(self.config["twitter_handle"]))
            return

        running_jobs.append(self.config)

        def run_check():
            while True:
                self.poster_obj.send()
                sleep(self.check_delay)
        thread = threading.Thread(target=run_check)
        thread.start()

