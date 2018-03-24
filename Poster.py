import requests


class Poster:
    def __init__(self, watcher, webhook):
        self.watcher = watcher
        self.url = webhook
        self.text_enabled = True
        self.images_enabled = True
        self.link_enabled = True

    # functions for enabling/disabling sending images and text to the webhook
    def enable_text(self):
        self.text_enabled = True

    def enable_images(self):
        self.images_enabled = True

    def enable_links(self):
        self.link_enabled = True

    def disable_text(self):
        self.text_enabled = False

    def disable_images(self):
        self.images_enabled = False

    def disable_links(self):
        self.link_enabled = False

    # checks the assigned watcher for a new tweet, if so it sends it to the webhook
    def send(self):
        if not self.watcher.check():
            return

        text = self.watcher.get("text")
        image = self.watcher.get("image")
        link = self.watcher.get("url")
        if not text:
            text = ""
        if not image:
            image = ""
        if not link:
            link = ""

        data = {"content": ""}
        if self.text_enabled:
            data["content"] += text

        if self.images_enabled:
            data["content"] += image

        if self.link_enabled:
            data["content"] += link
        requests.post(self.url, data)
