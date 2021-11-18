import praw
import configparser
import time
import schedule

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


keywords = read_trigger_file("keywords.txt")
summon = read_trigger_file("summon.txt")
blockresponse = read_trigger_file("blockresponse.txt")


def poll():
    timestamp_cutoff = current_seconds_time() - 10*60
    print(timestamp_cutoff)

    reddit = praw.Reddit(client_id=config['creds']['id'], client_secret=config['creds']['secret'],
                         password=config['creds']['pass'], user_agent="foodsafebotV" + version,
                         username=config['creds']['user'])
    me = reddit.redditor(config['creds']['user'])
    responded_to = set([x.link_id for x in me.comments.new(limit=100)])
    print(responded_to)
    subreddit = reddit.subreddit("3dprinting")

    for submission in subreddit.new(limit=20):
        if submission.created_utc < timestamp_cutoff:
            break
        if any(k in submission.title.lower() for k in keywords):
            print("Replying to sumbmission " + str(submission) + " " + str(submission.title))
            # submission.reply(response)

    for comment in subreddit.comments(limit=100):
        if comment.author.id == me.id or any(b in blockresponse for b in comment.body.lower()) or any(b in blockresponse for b in comment.author.lower()):
            continue
        if comment.created_utc < timestamp_cutoff:
            break
        if any(k in comment.body.lower() for k in summon):
            print("Replying to summon " + str(comment))
            # comment.reply("I have been summoned! \n\n" + response)
        elif any(k in comment.body.lower() for k in keywords) and comment.link_id not in responded_to:
            print("Replying to comment " + str(comment) + " " + str(comment.body))
            # comment.reply(response)


schedule.every(10).minutes.do(poll)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(50)
    # poll()
