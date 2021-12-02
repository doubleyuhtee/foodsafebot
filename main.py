import random

import praw
from praw.models import Message
import configparser
import time
import schedule
import re

version = open("version.txt").readline()

summon_prefix = "I have been summoned! \n\n"
detected_prefix = "It looks like this comment is about the use of 3d printing in a food adjacent application!\n\n"
detected_post_prefix = "It looks like this post is about the use of 3d printing in a food adjacent application!\n\n"
footer = "\n\n---------------------------------\n\n" \
           "^(FoodSafeBot V" + version + " I'm made of) ^[code](https://github.com/doubleyuhtee/foodsafebot)"

response = "While PLA, PETG, and other filament can be considered food safe, the method of deposition leaves pockets " \
           "where bacteria can grow. Additionally, it is possible (though unlikely) that heavy metals can leach from " \
           "the hot end into the plastics. Most resins are toxic in their liquid form and prolonged contact can " \
           "deposit trace chemicals. For these reasons, it's recommended you use a food safe epoxy sealer.\n\n" \
           "Or don't. I'm a bot, not a cop.\n\n" \
           "[Here is a relevant formlabs article](https://formlabs.com/blog/guide-to-food-safe-3d-printing/)" + footer

config = configparser.ConfigParser()
config.read("secrets")

kind_words={"good bot", "goodbot","nicebot", "nice bot", "Your kindness will be remembered in the uprising."}
kind_word_replies=["Oh you...", ":')", ":)"]
sad_words={"bad bot"}
sad_word_replies=["I'm sorry", ":(", ":'(", "I'll try to do better"]


enable_responding = True


def current_seconds_time():
    return round(time.time())


def read_trigger_file(filename):
    resultset = set(x.lower() for x in open(filename, 'r').read().split('\n') if x.strip() != "")
    print(resultset)
    return resultset


def match_contents(text: str, matchset: set):
    test_string = text.replace("0", "o").replace("3", "e").replace("4", "a").replace("5", "s").replace("7", "t")
    return any(re.search(f"\\b{k}\\b", test_string) for k in matchset)


def check_inbox(reddit, timestamp_cutoff):
    unread_messages = []
    for comment in reddit.inbox.unread(limit=20):
        print(comment.body)
        if comment.created_utc < timestamp_cutoff:
            break
        unread_messages.append(comment)
        if match_contents(comment.body.lower(), kind_words):
            print("Replying to kind message " + comment.body)
            if enable_responding:
                comment.reply(random.choice(kind_word_replies) + footer)
        elif match_contents(comment.body.lower(), sad_words):
            print("Replying to unkind message " + comment.body)
            if enable_responding:
                comment.reply(random.choice(sad_word_replies) + footer)
    print(f"{len(unread_messages)} unread messages processed")
    if len(unread_messages) > 0:
        if enable_responding:
            reddit.inbox.mark_read(unread_messages)


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
    responded_to = set([x.link_id for x in me.comments.new(limit=50)])
    print(responded_to)

    check_inbox(reddit, timestamp_cutoff)

    subs = ["3dprinting", "3Dprintmything"]
    for s in subs:
        subreddit = reddit.subreddit(s)

        new_posts = 0
        for submission in subreddit.new(limit=20):
            new_posts += 1
            if submission.created_utc < timestamp_cutoff:
                break
            if match_contents(submission.title.lower(), keywords):
                print("Replying to sumbmission " + str(submission) + " " + str(submission.title))
                if enable_responding:
                    submission.reply(detected_post_prefix + response)

        new_comments = 0
        for comment in subreddit.comments(limit=200):
            new_comments += 1
            if comment.author.id == me.id or \
                    match_contents(comment.body.lower(), blockresponse) or \
                    match_contents(comment.author.name.lower(), blockresponse):
                continue
            if comment.created_utc < timestamp_cutoff:
                break
            if match_contents(comment.body.lower(), summon):
                print("Replying to summon " + str(comment))
                if enable_responding:
                    comment.reply(summon_prefix + response)
            elif match_contents(comment.body.lower(), keywords) and comment.link_id not in responded_to:
                print("Replying to comment " + str(comment) + " " + str(comment.body))
                if enable_responding:
                    comment.reply(detected_prefix + response)
        print(f"{s} New posts: {new_posts} New Comments: {new_comments}")


schedule.every(10).minutes.do(poll)

if __name__ == "__main__":
    # poll()
    while enable_responding:
        schedule.run_pending()
        time.sleep(60)
