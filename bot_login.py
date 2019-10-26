import praw
import os

def bot_login():
    print("Logging in...")
    try:
        # reddit_instance = praw.Reddit(username=os.environ["username"],
        #                      password=os.environ["password"],
        #                      client_id=os.environ["client_id"],
        #                      client_secret=os.environ["client_secret"],
        #                      user_agent=os.environ["user_agent"])
        reddit_instance = praw.Reddit('bot1')
        print("Logged in!")
    except:
        print("Failed to log in!")
    return reddit_instance
