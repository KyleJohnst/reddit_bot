import praw
import os
import re

reddit = praw.Reddit('bot1')

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

for submission in reddit.subreddit('KyleDevEnv').new(limit=25):
    print(submission.title)

    if any(word in submission.title.lower() or word in submission.selftext.lower() for word in values):
        if submission.id not in posts_replied_to:
                # Reply
                submission.reply("If you have any medical concerns in regards to diving, you should contact [DAN](https://www.diversalertnetwork.org/) for medical advice. The opinions here should not superceed that of a trained medical practioner.")
                print("Bot replying to : ", submission.title)

                # Store id in response list
                posts_replied_to.append(submission.id)

# Write updated list to file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
