import tweepy
import time
import config as cfg
import os

# Retrieve API keys from config
CONSUMER_KEY = cfg.key_config["consumer_key"]
CONSUMER_SECRET = cfg.key_config["consumer_secret"]
ACCESS_KEY = cfg.key_config["access_key"]
ACCESS_SECRET = cfg.key_config["access_secret"]

# Establish file location of previous tweet IDs (Could be a database)
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(THIS_FOLDER, cfg.file_config["file_name"])

# Authenticate connection to twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def save_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    print("retrieving and replying to tweets...")
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode="extended")

    for mention in reversed(mentions):
        print(str(mention.id) + " - " + mention.full_text)
        last_seen_id = mention.id
        save_last_seen_id(last_seen_id, FILE_NAME)

        entities = mention.entities
        for hashtag in entities["hashtags"]:
            if (hashtag["text"].lower() == "helloworld"):
                print("Hello to you too")
                api.update_status("@" + mention.user.screen_name +
                                  "#HelloWorld back to you!", mention.id)


while True:
    reply_to_tweets()
    time.sleep(15)
