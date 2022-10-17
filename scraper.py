import praw
import os
from dotenv import load_dotenv
from requests_html import HTMLSession
import json
import re

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)


session=HTMLSession()
resRisers=[]
resFallers=[]

for submission in reddit.subreddit("FantasyPL").hot(limit=1000):
    if "Player Price Changes" in submission.title:
        pageHtml = session.get(submission.url)
        tableRisers = pageHtml.html.find("table")[0]
        tableFallers = pageHtml.html.find("table")[1]
        risersData = [[re.sub('[\u00a3%]', '', cell.text) for cell in row.find("td")] for row in tableRisers.find("tr")][1:]
        fallersData = [[re.sub('[\u00a3%]', '', cell.text) for cell in row.find("td")] for row in tableFallers.find("tr")][1:]
        headerData = [[re.sub("\u2206", 'Delta', cell.text) for cell in row.find("th")] for row in tableRisers.find("tr")][0]
        headerData.insert(0,"Date")
        for i in risersData:
            i.insert(0,submission.created_utc*1000)
        for i in fallersData:
            i.insert(0,submission.created_utc*1000)
                        
        resRisers.append([dict(zip(headerData, data)) for data in risersData])
        resFallers.append([dict(zip(headerData, data)) for data in fallersData])
        
with open("risers.json", "w") as f:
     json.dump(resRisers, f)
with open("fallers.json", "w") as f:
     json.dump(resFallers, f)
    # if "Top 10 Net Transfers In and Out" in submission.title:
    #     print(submission.title)    
