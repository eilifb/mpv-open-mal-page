#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
doc
"""
import sys
import requests
import urllib.parse
import webbrowser

from guessit import guessit


def main():
    file_path = sys.argv[1]
    mal_id = sys.argv[2]

    print("filepath: %s" % (file_path))
    guessit_match = guessit(file_path)

    for key, match in guessit_match.items():
        print("GuessIt: %s - %s" % (key, match))

        pass

    mal_url = "https://api.myanimelist.net/v2/anime"
    params = {"q": urllib.parse.quote_plus(guessit_match["title"]), "limit": 1}

    if "year" in guessit_match:
        params["start_date"] = f"{guessit_match["year"]}-01-01"

    response = requests.get(
        mal_url, params=params, headers={"X-MAL-CLIENT-ID": mal_id}
    )

    print("MAL response: %i" % (response.status_code))

    if response.status_code == 200:
        result = response.json()
        if result["data"]:
            anime_url = (
                f"https://myanimelist.net/anime/{result['data'][0]['node']['id']}"
            )
            print("Found match!: %s" % (anime_url))
            webbrowser.open_new_tab(anime_url)
            sys.exit(0)
        else:
            print("No match!")
            sys.exit(1)
    else:
        print("Unexpected response code!")
        sys.exit(2)


if __name__ == "__main__":
    main()
