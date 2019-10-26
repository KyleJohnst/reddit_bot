import praw
import os
import re
import bot_login
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
TimeLim = currentDT - 3600.00 # 1 Hour limit

def eanxCalc(param):
    try:
        measurement = param[-1]
        if measurement == 'm':
            x = 1.4/(int(param[0])/10+1)
            eanx = x * 100
            return int(eanx)
        elif measurement == 'ft':
            conv = int(param[0])/3.2808
            x = 1.4/(conv/10+1)
            eanx = x * 100
            return int(eanx)
    except Exception as exc:
        print("Failed nitrox percentage calculation with exc: ", exc)


botTag = "\n\n\n\n---\n\n^(Beep boop. I am a baby bot and still make mistakes . If there are any issues, contact my) [^Master ](https://www.reddit.com/message/compose/?to=Aer0za&subject=/u/DiveBotto)\n\n^(Check out my ) [^GitHub ](https://github.com/KyleJohnst/reddit_bot)"

try:
    # Monitor new posts stream
    for submission in reddit.subreddit(os.environ["KyleDevEnv"]).stream.submissions():
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
                    submission.reply("If you have any medical concerns in regards to diving accidents or emergencies, you should contact [DAN Emergency Numbers](http://danap.org/inside/hotlines.php)." + "\n\n\n For non-emergency communication use these links below" + "\n\n\n [DAN North America](https://www.diversalertnetwork.org/contact/)" + "\n\n [DAN Brasil](https://www.danbrasil.org.br/contescritorio)" +  "\n\n [DAN Europe](https://www.daneurope.org/web/guest/contacts#p_p_id_56_INSTANCE_l42C_)" + "\n\n [DAN Southern Africa](https://www.dansa.org/contact)" + "\n\n [DAN Asia Pacific](http://danap.org/contact_dan/asiapacificoffices.php)" + "\n\n [DAN Japan](https://www.danjapan.gr.jp/form/contact)" + "\n\n [DAN World](http://world.dan.org/contact-danworld)" + "\n\n The opinions of members here should not supersede that of a trained medical practioner." + botTag)
                    print("Bot replying to : ", submission.title)
                    # Store id in response list
                    posts_replied_to.append(submission.id)

except Exception as exc:
    print("Process failed to respond to new submissions with exc: ", exc)

try:
    for comment in reddit.subreddit('KyleDevEnv').stream.comments():
            if comment.created_utc > TimeLim:
                context = comment.body.lower().split(' ')
                for keyword in context:
                    if keyword == 'nitrox%':
                        parameter = context.pop(1)
                        params = parameter.split('/')
                        eanx = str(eanxCalc(params))
                        if eanx != 'None':
                            comment.reply("Hello, the maximum O^2 percentage for your dive to a maximum depth of" + params[0] + params[-1] + ", would be " + eanx + "%. Rounded down for conservatism with a PO^2 of 1.4" + "\n\n\n This is just a guidline and should not replace your own calculations" + botTag)
                            print("Replying with max O2 percentage to: ", comment.body)
                        else:
                            comment.reply("Hello, you will need to specify wether I need to work from feet or meters, please call again using the format of max_depth/ft or max_depth/m" + botTag)
                            print("Educating person: ", comment.body)

except Exception as exc:
    print("Process failed with exc: ", exc)

# Write updated list to file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
