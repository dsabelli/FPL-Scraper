import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

for submission in reddit.subreddit("FantasyPL").hot(limit=10000):
    if "Player Price Changes" in submission.title:
        print(submission.title)