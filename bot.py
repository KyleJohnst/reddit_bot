import praw
import os
import re
import bot_login
import datetime
import time

reddit = bot_login.bot_login()

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

currentDT = time.time()
TimeLim = currentDT - 43200.00 # 12 Hour limit

try:
    # Monitor new posts stream
    for submission in reddit.subreddit('scuba').stream.submissions():
        print(submission.title)

        # Ensure bot only responds to posts from last 12 hours
        if submission.created_utc > TimeLim:
            # Break up the data in the submission to allow more accurate verification
            header = submission.title.lower().split(' ')
            content = submission.selftext.lower().split(' ')
            # Check for keywords
            if any(word in header or word in content for word in values):
                if submission.id not in posts_replied_to:
                    # Reply
                    submission.reply("If you have any medical concerns in regards to diving accidents or emergencies, you should contact [DAN Emergency Numbers](http://danap.org/inside/hotlines.php)." + "\n\n\n For non-emergency communication use these links below" + "\n\n\n [DAN North America](https://www.diversalertnetwork.org/contact/)" + "\n\n [DAN Brasil](https://www.danbrasil.org.br/contescritorio)" +  "\n\n [DAN Europe](https://www.daneurope.org/web/guest/contacts#p_p_id_56_INSTANCE_l42C_)" + "\n\n [DAN Southern Africa](https://www.dansa.org/contact)" + "\n\n [DAN Asia Pacific](http://danap.org/contact_dan/asiapacificoffices.php)" + "\n\n [DAN Japan](https://www.danjapan.gr.jp/form/contact)" + "\n\n [DAN World](http://world.dan.org/contact-danworld)" + "\n\n The opinions of members here should not supersede that of a trained medical practioner." + "\n\n\n\n---\n\n^(Beep boop. I am a baby bot and still make mistakes . If there are any issues, contact my) [^Master ](https://www.reddit.com/message/compose/?to=Aer0za&subject=/u/DiveBotto)\n\n^(Check out my ) [^GitHub ](https://github.com/KyleJohnst/reddit_bot)")
                    print("Bot replying to : ", submission.title)
                    # Store id in response list
                    posts_replied_to.append(submission.id)
        else:
            print("Posted EXCEEDED new post time limit and wont be responded to.")

except Exception as exc:
    pass
    print("Process failed with exc: ", exc)

# Write updated list to file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
