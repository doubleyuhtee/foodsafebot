import praw
import configparser
import time

version = open("version.txt").readline()

response = "It looks like this post is about the use of 3d printing in a food adjacent application!\n\n" \
           "While PLA filament is considered food safe, the method of deposition leaves pockets that bacteria " \
           "can grow in. Additionally, it is possible (though unlikely) that heavy metals can leach from the hot " \
           "end into the plastics. Most resins are toxic in their liquid form and prolonged contact can deposit " \
           "trace chemicals. For these reasons, it's recommended you use a food safe epoxy sealer.\n\n" \
           "Or don't, I'm a bot, not a cop.\n\n---------------------------------\n\n" \
           "^(FoodSafeBot V" + version + " I'm made of) ^[code](https://github.com/doubleyuhtee/foodsafebot)"


def current_seconds_time():
    return round(time.time())


def read_trigger_file(filename):
    return open(filename, 'r').read().split('\n')


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("secrets")

    reddit = praw.Reddit(client_id=config['creds']['id'], client_secret=config['creds']['secret'],
                         password=config['creds']['pass'], user_agent="foodsafebotV" + version,
                         username=config['creds']['user'])

    keywords = read_trigger_file("keywords.txt")
    summon = read_trigger_file("summon.txt")
    timestamp_cutoff = current_seconds_time() - 10*60

    subreddit = reddit.subreddit("3dprinting")

    for submission in subreddit.new(limit=20):
        if submission.created_utc < timestamp_cutoff:
            break
        if any(k in submission.title.lower() for k in keywords):
            print("Replying to sumbmission " + submission)
            submission.reply(response)

    for comment in subreddit.comments(limit=100):
        if comment.created_utc < timestamp_cutoff:
            break
        if any(k in comment.body.lower() for k in summon):
            print("Replying to summon " + str(comment))
            comment.reply("I have been summoned! \n\n" + response)
        elif any(k in comment.body.lower() for k in keywords):
            print("Replying to comment " + str(comment))
            comment.reply(response)
