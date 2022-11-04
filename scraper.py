import praw
import os
from dotenv import load_dotenv
from requests_html import HTMLSession
import json
import re
from datetime import datetime

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)


session=HTMLSession()
resRisers=[]
resFallers=[]
resIn=[]
resOut=[]

# print(datetime.utcfromtimestamp(1665797463).strftime("%Y-%m-%d"))

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
            i.insert(0,datetime.utcfromtimestamp(submission.created_utc).strftime("%Y-%m-%d"))
        for i in fallersData:
            i.insert(0,datetime.utcfromtimestamp(submission.created_utc).strftime("%Y-%m-%d"))
                        
        resRisers.append([dict(zip(headerData, data)) for data in risersData])
        resFallers.append([dict(zip(headerData, data)) for data in fallersData])
        
    if "Top 10 Net Transfers In and Out" in submission.title:
        pageHtml = session.get(submission.url)
        tableIn = pageHtml.html.find("table")[0]
        tableOut = pageHtml.html.find("table")[1]
    
        inData = [[re.sub('%', '', cell.text) for cell in row.find("td")] for row in tableIn.find("tr")][1:]
        outData = [[re.sub('%', '', cell.text) for cell in row.find("td")] for row in tableOut.find("tr")][1:]
        headerData = [[ cell.text for cell in row.find("th")] for row in tableIn.find("tr")][0]
        
        headerData.insert(0,"Date")
        for i in inData:
            i.insert(0,datetime.utcfromtimestamp(submission.created_utc).strftime("%Y-%m-%d"))
        for i in outData:
            i.insert(0,datetime.utcfromtimestamp(submission.created_utc).strftime("%Y-%m-%d"))
    
        resIn.append([dict(zip(headerData, data)) for data in inData])
        resOut.append([dict(zip(headerData, data)) for data in outData])
        
with open("risers.json", "w") as f:
     json.dump(resRisers, f)
with open("fallers.json", "w") as f:
     json.dump(resFallers, f)
with open("in.json", "w") as f:
     json.dump(resIn, f)
with open("out.json", "w") as f:
     json.dump(resOut, f)
  
