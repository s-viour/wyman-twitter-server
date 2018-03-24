import json
import tweepy


class Watcher:
    def __init__(self, user_name):
        self.user_name = user_name
        self.consumer_key = None
        self.consumer_secret = None
        # while the last tweet will be stored in a local file, last_tweet will hold it in memory
        self.last_tweet = {}
        self.last_tweet_id = ""
        self.api = None

        # load and set config variables
        with open("./config.json", "r") as f:
            config = json.loads(f.read())
            self.consumer_key = config["consumer_key"]
            self.consumer_secret = config["consumer_secret"]

        # check whether consumer_key or consumer_secret is blank
        if not self.consumer_key or not self.consumer_secret:
            raise Exception("consumer key or consumer secret is blank!")

        # validate the credentials with the twitter api
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        try:
            self.api = tweepy.API(auth)
        except tweepy.TweepError:
            raise Exception("consumer key or consumer secret is invalid!")

    # returns True if a new tweet has been posted since the last check
    def check(self):
        tweet_id = self.api.user_timeline(id=self.user_name, count=1, tweet_mode="extended", exclude_replies=True)[0]._json["id_str"]
        if tweet_id != self.last_tweet_id:
            self.last_tweet_id = tweet_id
            self.last_tweet = self.api.user_timeline(id=self.user_name, count=1, tweet_mode="extended", exclude_replies=True)[0]._json
            return True
        return False

    # used to grab various parts of the latest recorded tweet
    # value list: 'id', 'date', 'url', 'image', 'text'
    def get(self, what):
        if what == "id":
            return self.last_tweet["id_str"]
        elif what == "date":
            return self.last_tweet["created_at"]
        elif what == "url":
            # it works this time i swear
            return "https://twitter.com/" + self.user_name + "/status/" + self.get("id")
        elif what == "image":
            try:
                image = self.last_tweet["entities"]["media"][0]["media_url_https"]
            except KeyError:
                image = False
            return image
        elif what == "text":
            try:
                text = self.last_tweet["full_text"]
            except KeyError:
                text = False
            return text

    # function for checking if the tweet has an image or any text attached
    def has(self, what):
        string = ""
        if what == "image":
            string = self.get("image")
        elif what == "text":
            string = self.get("text")
        if string == "":
            return False
        return True
