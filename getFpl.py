import urllib.request
import json
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

response = urllib.request.urlopen(url)

data = response.read().decode('UTF-8')

jsonData = json.loads(data)

#connect to DB
con = psycopg2.connect(
     
     host = "fdaa:0:b764:a7b:88dc:3e44:f6f5:2",
     user = "postgres",
     password = "190aEQwqvS6L1FU",
     port=5432
)

#cursor
cur = con.cursor()

cur.execute("INSERT into fpl (season, gameweek, total_players, events, elements) values (%s,%s,%s,%s,%s);",("22/23", 15,json.dumps(jsonData["total_players"]), json.dumps(jsonData["events"]), json.dumps(jsonData["elements"])))

cur.execute("SELECT * FROM fpl")

rows = cur.fetchall()

print(rows)

# with open("players.json", "w") as f:
#      json.dump(jsonData["elements"], f)
# with open("gameWeeks.json", "w") as f:
#      json.dump(jsonData["events"], f)
# with open("total.json", "w") as f:
#      json.dump(jsonData["total_players"], f)
     
#close connection     
con.close()