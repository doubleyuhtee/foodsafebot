import praw
import configparser
import time
import schedule
import re

version = open("version.txt").readline()

response = "It looks like this post is about the use of 3d printing in a food adjacent application!\n\n" \
           "While PLA filament is considered food safe, the method of deposition leaves pockets that bacteria " \
           "can grow in. Additionally, it is possible (though unlikely) that heavy metals can leach from the hot " \
           "end into the plastics. Most resins are toxic in their liquid form and prolonged contact can deposit " \
           "trace chemicals. For these reasons, it's recommended you use a food safe epoxy sealer.\n\n" \
           "Or don't, I'm a bot, not a cop.\n\n---------------------------------\n\n" \
           "^(FoodSafeBot V" + version + " I'm made of) ^[code](https://github.com/doubleyuhtee/foodsafebot)"

config = configparser.ConfigParser()
config.read("secrets")


def current_seconds_time():
    return round(time.time())


def read_trigger_file(filename):
    resultset = set(x.lower() for x in open(filename, 'r').read().split('\n') if x.strip() != "")
    print(resultset)
    return resultset


def match_contents(text: str, matchset: set):
    return any(re.search("\b" + k + "\b", text) for k in matchset)


keywords = read_trigger_file("keywords.txt")
summon = read_trigger_file("summon.txt")
blockresponse = read_trigger_file("blockresponse.txt")


def poll():
    timestamp_cutoff = current_seconds_time() - 11*60
    print(timestamp_cutoff)

    reddit = praw.Reddit(client_id=config['creds']['id'], client_secret=config['creds']['secret'],
                         password=config['creds']['pass'], user_agent="foodsafebotV" + version,
                         username=config['creds']['user'])
    me = reddit.redditor(config['creds']['user'])
    responded_to = set([x.link_id for x in me.comments.new(limit=100)])
    print(responded_to)
    subreddit = reddit.subreddit("3dprinting")

    new_posts = 0
    for submission in subreddit.new(limit=20):
        new_posts += 1
        if submission.created_utc < timestamp_cutoff:
            break
        if match_contents(submission.title.lower(), keywords):
            print("Replying to sumbmission " + str(submission) + " " + str(submission.title))
        #     # submission.reply(response)

    new_comments = 0
    for comment in subreddit.comments(limit=100):
        new_comments += 1
        if comment.author.id == me.id or \
                match_contents(comment.body.lower(), blockresponse) or \
                match_contents(comment.author.name.lower(), blockresponse):
            continue
        if comment.created_utc < timestamp_cutoff:
            break
        if match_contents(comment.body.lower(), summon):
            print("Replying to summon " + str(comment))
            comment.reply("I have been summoned! \n\n" + response)
        elif match_contents(comment.body.lower(), keywords) and comment.link_id not in responded_to:
            print("Replying to comment " + str(comment) + " " + str(comment.body))
        #     # comment.reply(response)
    print(f"New posts: {new_posts} New Comments: {new_comments}")

schedule.every(10).minutes.do(poll)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
    # poll()
