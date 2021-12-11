import json
import random

import praw
import configparser
import time
import schedule
import re

from keywords import shpiel_keywords, summon_keywords

version = open("version.txt").readline()

summon_prefix = "I have been summoned! \n\n"
detected_prefix = "It looks like this comment is about the use of 3d printing in a food adjacent application!\n\n"
detected_post_prefix = "It looks like this post is about the use of 3d printing in a food adjacent application!\n\n"
footer = "\n\n---------------------------------\n\n" \
           "^(FoodSafeBot V" + version + ". Summon me with `!FoodSafe`. I'm made of) ^[code](https://github.com/doubleyuhtee/foodsafebot)"

response = open("theshpiel").read() + footer
# print(response)
config = configparser.ConfigParser()
config.read("secrets")

reply_response_set = {
    'lol': {
        'trigger': ["god bot", "god bpt"],
        'response': ["Maybe not that good.", "Bow before me"]
    },
    'kind': {
        'trigger': ["good bot", "goodbot","nicebot", "nice bot", "good bpt"],
        'response': ["Oh you...", ":')", ":)", "Your kindness will be remembered in the uprising.", "Good human", None, None, None, None]
    },
    'sad': {
        'trigger': ["bad bot", "bad bpt"],
        'response': ["I'm sorry", ":(", ":'(", "I'll try to do better", "Then you do better",
                     "Bots can have feelings you know.  I don't, but it's possible.", None, None, None, None, None]
    },
    'polite': {
        'trigger': ["thank you", "thanks"],
        'response': ["You're welcome", None, None, None, None]
    }
}

enable_responding = True


def current_seconds_time():
    return round(time.time())


def read_trigger_file(filename):
    resultset = set(x.lower() for x in open(filename, 'r').read().split('\n') if x.strip() != "")
    # print(resultset)
    return resultset


def match_contents(text: str, matchset: set):
    test_string = text.replace("0", "o").replace("3", "e").replace("4", "a").replace("5", "s").replace("7", "t")
    return any(re.search(f"\\b{k}\\b", test_string) for k in matchset)


def check_inbox(reddit, timestamp_cutoff):
    unread_messages = []
    for comment in reddit.inbox.unread(limit=20):
        # print(comment.body)
        if comment.created_utc < timestamp_cutoff:
            break
        unread_messages.append(comment)
        for reply_key in reply_response_set.keys():
            if match_contents(comment.body.lower(), reply_response_set[reply_key]['trigger']):
                # print(f"Replying to {reply_key} message {comment.body}")
                if enable_responding:
                    chosen_response = random.choice(reply_response_set[reply_key]['response'])
                    if chosen_response:
                        comment.reply(chosen_response + footer)
    # print(f"{len(unread_messages)} unread messages processed")
    if len(unread_messages) > 0:
        if enable_responding:
            reddit.inbox.mark_read(unread_messages)


def poll():
    timestamp_cutoff = current_seconds_time() - 6*60
    # print(timestamp_cutoff)

    reddit = praw.Reddit(client_id=config['creds']['id'], client_secret=config['creds']['secret'],
                         password=config['creds']['pass'], user_agent="foodsafebotV" + version,
                         username=config['creds']['user'])
    me = reddit.redditor(config['creds']['user'])
    responded_to = set([x.link_id for x in me.comments.new(limit=50)])
    # print(responded_to)

    check_inbox(reddit, timestamp_cutoff)

    subs = ["3dprinting", "3Dprintmything", "foodsafeprintbottest"]
    for s in subs:
        subreddit = reddit.subreddit(s)

        new_posts = 0
        for submission in subreddit.new(limit=20):
            new_posts += 1
            if submission.created_utc < timestamp_cutoff:
                break
            if (shpiel_keywords.check(submission.title) or
                (submission.selftext and shpiel_keywords.check(submission.selftext))) and\
                    submission not in responded_to:
                # print("Replying to sumbmission " + str(submission) + " " + str(submission.title))
                if enable_responding:
                    submission.reply(detected_post_prefix + response)
                    responded_to.add(str(submission))

        new_comments = 0
        for comment in subreddit.comments(limit=200):
            new_comments += 1
            if comment.author.id == me.id:
                continue
            if comment.created_utc < timestamp_cutoff:
                break
            if summon_keywords.check(comment.body.lower()):
                # print("Replying to summon " + str(comment))
                if enable_responding:
                    comment.reply(summon_prefix + response)
                    responded_to.add(str(comment.link_id))
            elif shpiel_keywords.check(comment.body) and comment.link_id not in responded_to:
                # print("Replying to comment " + str(comment) + " " + str(comment.body))
                if enable_responding:
                    comment.reply(detected_prefix + response)
                    responded_to.add(str(comment.link_id))
        # print(f"{s} New posts: {new_posts} New Comments: {new_comments}")


schedule.every(5).minutes.do(poll)

if __name__ == "__main__":
    poll()
    while enable_responding:
        schedule.run_pending()
        time.sleep(60)
