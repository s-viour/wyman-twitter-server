import requests


class Poster:
    def __init__(self, watcher, webhook):
        self.watcher = watcher
        self.url = webhook
        self.text_enabled = True
        self.images_enabled = True

    # functions for enabling/disabling sending images and text to the webhook
    def enable_text(self):
        self.text_enabled = True

    def enable_images(self):
        self.images_enabled = True

    def disable_text(self):
        self.text_enabled = False

    def disable_images(self):
        self.images_enabled = False

    # checks the assigned watcher for a new tweet, if so it sends it to the webhook
    def send(self):
        if not self.watcher.check():
            print("watcher check failed")
            return

        text = self.watcher.get("text")
        image = self.watcher.get("image")
        if not text:
            text = ""
        if not image:
            image = ""

        data = None
        if self.text_enabled and self.images_enabled:
            print("both enabled")
            data = {
                "content": text + image
            }

        elif self.text_enabled and not self.images_enabled:
            print("only text enabled")
            data = {
                "content": text
            }

        elif not self.text_enabled and self.images_enabled:
            print("only images enabled")
            data = {
                "content": image
            }
        sent = requests.post(self.url, data)
        print(sent)
