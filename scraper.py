import praw
import os
from dotenv import load_dotenv
from requests_html import HTMLSession
import json

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)


session=HTMLSession()

for submission in reddit.subreddit("FantasyPL").hot(limit=30):
    if "Player Price Changes" in submission.title:
        pageHtml = session.get(submission.url)
        tableRisers = pageHtml.html.find("table")[0]
        tableFallers = pageHtml.html.find("table")[1]
        risersData = [[cell.text for cell in row.find("td")] for row in tableRisers.find("tr")][1:]
        fallersData = [[cell.text for cell in row.find("td")] for row in tableFallers.find("tr")][1:]
        headerData = [[cell.text for cell in row.find("th")] for row in tableRisers.find("tr")][0]
        
        resRisers = [dict(zip(headerData, data)) for data in risersData ]
        resFallers = [dict(zip(headerData, data)) for data in fallersData ]
        
        with open("risers.json", "w") as f:
            json.dump(resRisers, f)
        with open("fallers.json", "w") as f:
            json.dump(resFallers, f)
    # if "Top 10 Net Transfers In and Out" in submission.title:
    #     print(submission.title)    
    