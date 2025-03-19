#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tries to extract a Title and Year from a (media) filepath, and does a MAL API
query. If a match is found the program opens the corresponding MAL webpage.
Requires guessit (https://pypi.org/project/guessit/) and a MAL API Client ID.
"""
import sys
import io
import requests
import urllib.parse
import webbrowser
from difflib import SequenceMatcher as SM
from guessit import guessit

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def main():
    file_path = sys.argv[1]
    mal_id = sys.argv[2]
    title_match = bool(sys.argv[3])

    print("filepath: %s" % (file_path))
    guessit_match = guessit(file_path)

    for key, match in guessit_match.items():
        print("GuessIt: %s - %s" % (key, match))

        pass

    mal_url = "https://api.myanimelist.net/v2/anime"
    params = {
        "q": urllib.parse.quote_plus(guessit_match["title"]),
    }

    if "year" in guessit_match:
        params["q"] += f"+{guessit_match["year"]}"
    if title_match:
        params["fields"] = "alternative_titles"

    print(
        f"GET url: {mal_url}"
        "?"
        f"{"&".join([i[0]+"="+i[1] for i in params.items()])}"
    )
    response = requests.get(
        mal_url, params=params, headers={"X-MAL-CLIENT-ID": mal_id}
    )

    print("MAL response: %i" % (response.status_code))
    if response.status_code == 200:
        result = response.json()
        if result["data"]:  # If match found
            if title_match:
                nodes = [nodes["node"] for nodes in result["data"]]
                print("No. query results: %i" % (len(nodes)))
                print("First match title %s" % (nodes[0]["title"]))
                for entry in nodes:
                    # If the title guessit found matches the 'primary title':
                    print(
                        "comp. titles: %s <-> %s (%.3f)"
                        % (
                            guessit_match["title"],
                            entry["title"],
                            SM(None, guessit_match["title"], entry["title"]).ratio(),
                        )
                    )
                    if guessit_match["title"] == entry["title"]:
                        open_mal_page(entry["id"])
                        sys.exit(0)

                    # Checking against all alternative titles
                    for alt_title in titles_to_list(
                        entry["alternative_titles"]
                    ):
                        print(
                            "comp. titles: %s <-> %s (%.3f)"
                            % (
                                guessit_match["title"],
                                alt_title,
                                SM(None, guessit_match["title"], alt_title).ratio(),
                            )
                        )
                        if guessit_match["title"] == alt_title:
                            open_mal_page(entry["id"])
                            sys.exit(0)
                print("No exact match found!")
                sys.exit(3)

            open_mal_page(result["data"][0]["node"]["id"])
            sys.exit(0)
        else:
            print("No match!")
            sys.exit(1)
    else:
        print("Unexpected response code!")
        sys.exit(2)


def open_mal_page(id: str):
    anime_url = f"https://myanimelist.net/anime/{id}"
    webbrowser.open_new_tab(anime_url)
    print("Found match!: %s" % (anime_url))


def titles_to_list(json_data: dict):
    title_list = []
    for elem in json_data.values():
        if type(elem) is list:
            title_list += elem
        elif type(elem) is dict:
            # Doubt this ever happens, but the MAL API documentation
            # is kinda dogwater, so better be safe.
            title_list += titles_to_list(elem)
        else:
            title_list.append(elem)
    return title_list


if __name__ == "__main__":
    main()
