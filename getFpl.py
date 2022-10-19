import urllib.request
import json

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

response = urllib.request.urlopen(url)

data = response.read().decode('UTF-8')

jsonData = json.loads(data)



with open("players.json", "w") as f:
     json.dump(jsonData["elements"], f)
with open("gameWeeks.json", "w") as f:
     json.dump(jsonData["events"], f)
with open("total.json", "w") as f:
     json.dump(jsonData["total_players"], f)