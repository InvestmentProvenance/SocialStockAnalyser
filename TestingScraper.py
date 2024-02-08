import praw
import pandas as pd
from praw.models import MoreComments

reddit = praw.Reddit(
    client_id="wsewHa7zHhUasFHQYlEDSw",
    client_secret="G8k9dtn7mp3MD5WLSCsmwubmPcZ6vA",
    user_agent="my user agent",
)
subreddit = reddit.subreddit("wallstreetbets")
print(reddit.read_only)
i = 0
for submission in subreddit.hot(limit=2000):
    print(i)
    print(submission.title)
    # Output: the submission's title
    #print(submission.score)
    # Output: the submission's score
    # Output: the submission's ID
    i += 1
    #print(list(submission.comments))