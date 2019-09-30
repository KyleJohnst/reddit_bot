import praw
import os
import re

reddit = praw.Reddit(username = os.environ["username"],
                password = os.environ["password"],
                client_id = os.environ["client_id"],
                client_secret = os.environ["client_secret"],
                user_agent = os.environ["user_agent"])

# Create a list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# Or load the list of posts we have replied to
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

values = []
for keyword in open('keywords.txt'):
    values.append(keyword.strip('\n'))

try:
   # Monitor new posts stream  
   for submission in reddit.subreddit('KyleDevEnv').stream.submissions():
        print(submission.title)

        header = submission.title.lower().split(' ')
        content = submission.selftext.lower().split(' ')
    #Check for keywords
        if any(word in header or word in content for word in values):
            if submission.id not in posts_replied_to:
                # Reply
                submission.reply("If you have any medical concerns in regards to diving, you should contact [DAN Emergency Numbers](http://danap.org/inside/hotlines.php) for medical advice in case of a emergency. The opinions here should not supersede that of a trained medical practioner." + "\n\n\n\n---\n\n^(Beep boop. I am a baby bot and still make mistakes . If there are any issues, contact my) [^Master ](https://www.reddit.com/message/compose/?to=Aer0za&subject=/u/DiveBotto)\n\n^(Check out my ) [^GitHub ](https://github.com/KyleJohnst/reddit_bot)")
                print("Bot replying to : ", submission.title)

                # Store id in response list
                posts_replied_to.append(submission.id)
except Exception as exc:
    pass
    print("Process failed with exc: ", exc)

# Write updated list to file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")