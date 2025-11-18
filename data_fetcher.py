import requests
import pandas as pd
import time


def fetch_top_games(pages=2):
    """
    SteamSpy allows requesting games sorted by owners.
    page 0 = rank 1–1000, page 1 = 1001–2000, etc.
    We take the top 2000 for good coverage (includes almost all relevant indie hits).
    """
    all_games = []
    base_url = "https://steamspy.com/api.php"

    for page in range(pages):
        params = {
            "request": "top1000forever",
            "page": page
        }
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Error on page {page}: {response.status_code}")
            continue

        data = response.json()
        for appid, info in data.items():
            info["appid"] = int(appid)
            all_games.append(info)
        print(f"Page {page + 1}/{pages} downloaded ({len(all_games)} games so far)")
        time.sleep(0.5)  # Be nice to the server

    df = pd.DataFrame(all_games)
    return df