import praw
import configparser

if __name__ == "__main__":
    version = open("version.txt").readline()
    config = configparser.ConfigParser()
    config.read("secrets")

    reddit = praw.Reddit(client_id=config['creds']['id'], client_secret=config['creds']['secret'],
                         password=config['creds']['pass'], user_agent="foodsafebotV" + version,
                         username=config['creds']['user'])

    reddit.subreddit("test").submit("Test Submission", url="https://reddit.com")
