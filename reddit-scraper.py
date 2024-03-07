import praw
from praw.models import MoreComments
from datetime import datetime
from database import db_stock
import re

ticker = "nio"


def commentsFromSubreddit(url,reddit):
    dataList = []
    match = re.match(r"/r/([^/]+)/comments/([^/]+)/", url)
    if match:
        subreddit_name, post_id = match.groups()
    else:
        print("Invalid URL format.")
        return

    # Get the submission
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)

    for comment in submission.comments.list():
        dataList.append([str(comment.author),datetime.fromtimestamp(comment.created_utc),comment.body.replace("\n"," "),comment.score,"reddit.com","GME"])
        #username, timestamp, body, score, site, symbol)
        
    return(dataList)


"""
with open('uploadedPosts.txt', 'r') as file:
    content = file.read()
    visitednames = content.split(',')
    visitednames = [name.strip() for name in visitednames]# all posts that have already been read
"""



reddit = praw.Reddit(
    client_id="wsewHa7zHhUasFHQYlEDSw",
    client_secret="G8k9dtn7mp3MD5WLSCsmwubmPcZ6vA",
    user_agent="my user agent",
)

subreddit = reddit.subreddit("wallstreetbets")
search_results = subreddit.search(ticker,limit = None)
f = open("uploadedPosts.txt", "w")
n = 0
total = 0
for post in search_results:
    f.write(post.name)
    f.write(", ")
    if True: #not(post.name in visitednames):
        databaseEntry = commentsFromSubreddit(post.permalink,reddit)
        databaseEntry.append([str(post.author),datetime.fromtimestamp(post.created_utc),(post.title+post.selftext).replace("\n"," "),post.score,"reddit.com",ticker.upper()])
        db_stock.upload_sns(raw_data = databaseEntry)
        n+=1
        total = total + len(databaseEntry)
        print(n)
        print(total)
        print("\n\n")
print(":)")
f.close()
print(n)

