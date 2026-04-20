import json
import requests
import time
'''Code used to fetch data from RAWG API'''

API_KEY = "7fc9c356e3594e1eb89240cf3088018b"
url = "https://api.rawg.io/api/games"
params = {
    "key": API_KEY,
    "page_size": 40,        # max per page
    "ordering": "-rating",  # highest rated game first
    "page": 1
}
games = []
for page in range(1, 40):    # 7–8 pages for around 280 games
    params["page"] = page
    resp = requests.get(url, params=params).json()
    games.extend(resp["results"])
    print(f"Fetched page {page}, total: {len(games)}")
    time.sleep(0.2)
    if len(games) >= 1500:
        break

with open("games_raw_1500.json", "w") as f:
    json.dump(games, f, indent=2)