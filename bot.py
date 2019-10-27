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
TimeLim = currentDT - 300.00 # 5 min limit to respond to posts/comments

#Formula for working out EANx percentage for given depth.
# # PO2/P = FO2
def eanxCalc(param):
    try:
        measurement = param[-1]
        # Calculation for meters
        if measurement == 'm':
            x = 1.4/(int(param[0])/10+1)
            eanx = x * 100
            return int(eanx)
        # Calculation for feet
        elif measurement == 'ft':
            conv = int(param[0])/3.2808
            x = 1.4/(conv/10+1)
            eanx = x * 100
            return int(eanx)
    except Exception as exc:
        print("Failed nitrox percentage calculation with exc: ", exc)

# Formula for working out max depth for given EANx percentage
# PO2/FO2 = P
def depthCalc(param):
    try:
        d = 1.4/(float(param[0])/100.0)
        depth = (d - 1) * 10
        measurement = param[-1]
        #Convert from meters to feet or just returns meters
        if measurement == 'ft':           
            return int(depth*3.2808)
        else:
            return int(depth)
    except Exception as exc:
        print("Failed depth calculation with exc: ", exc)

#Tag for standard bot responses
botTag = "\n\n\n\n---\n\n^(Beep boop. I am a baby bot and still make mistakes . If there are any issues, contact my) [^Master ](https://www.reddit.com/message/compose/?to=Aer0za&subject=/u/DiveBotto)\n\n^(Check out my ) [^GitHub ](https://github.com/KyleJohnst/reddit_bot)"

# Monitor new posts stream for medical questions
try:
    for submission in reddit.subreddit(os.environ["subreddit"]).stream.submissions():
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

# Methods to monitor for EANx(Nitrox) calculation requests
try:
    for comment in reddit.subreddit(os.environ["subreddit"]).stream.comments():
            if comment.created_utc > TimeLim:
                context = comment.body.lower().split(' ')
                for keyword in context:
                    # Monitors for requests for EANx percentage requests
                    if keyword == 'nitrox%':
                        # Gets the parameters from the request
                        parameter = context.pop(1)
                        # Separates params into the variables needed
                        params = parameter.split('/')
                        #Get calculations
                        eanx = str(eanxCalc(params))
                        # Reply if calc passes or educate requester on needed format.
                        if eanx != 'None':
                            comment.reply("Hello, the maximum O^2 EANx percentage for your dive to a maximum depth of " + params[0] + params[-1] + ", would be " + eanx + "%. Rounded down for conservatism with a PO^2 of 1.4Bar" + "\n\n\n This is just a guideline and should not replace your own calculations and training" + botTag)
                            print("Replying with max O2 percentage to: ", comment.body)                           
                        else:
                            comment.reply("Hello, you will need to specify wether I need to work from feet or meters, please call again using the format of max_depth/ft or max_depth/m" + botTag)
                            print("Educating person: ", comment.body)
                    
                    # Monitors for max depth on percentage requests
                    if keyword == 'nitroxdepth':
                        # Gets the parameters from the request
                        parameter = context.pop(1)
                        # Separates params into the variables needed
                        params = parameter.split('/')
                        # Get calculations
                        depth = str(depthCalc(params))
                        # Reply if calc passes or educate requester on needed format.
                        if depth != 'None':
                            comment.reply("Hello, the maximum depth you could dive to on " + params[0] + "%" + " EANx would be " + depth + params[-1]+ ". Rounded down for conservatism and assuming a PO^2 of 1.4Bar" + "\n\n\n These responses should just be used as a guideline and not replace your own calculations and training" + botTag)
                            print("Replying with max depth to: ", comment.body)
                            posts_replied_to.append(comment.id)
                        else:
                            comment.reply("Hello, you will need to specify wether I need to work in feet or meters, please call again using the format of EANx/ft or EANx/m ie: 32/ft" + botTag)
                            print("Educating person: ", comment.body)
                            posts_replied_to.append(comment.id)
except Exception as exc:
    print("Process failed with exc: ", exc)

# Write updated list to file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
