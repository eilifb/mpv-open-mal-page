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
from urllib import parse
import webbrowser
from difflib import SequenceMatcher as SM
from guessit import guessit

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def main():
    file_path = sys.argv[1]
    mal_id = sys.argv[2]
    title_threshold = float(sys.argv[3])

    print("filepath: %s" % (file_path))
    guessit_match = guessit(file_path)

    for key, match in guessit_match.items():
        print("GuessIt: %s - %s" % (key, match))

    params = {
        "q": parse.quote_plus(guessit_match["title"]),
        "fields": "alternative_titles"
    }

    if "year" in guessit_match:
        params["q"] += f"+{guessit_match["year"]}"

    mal_url = "https://api.myanimelist.net/v2/anime"
    param_url = parse.urlencode(params)
    full_url = f"{mal_url}?{param_url}"

    print(f"GET url: {full_url}")

    response = requests.get(full_url, headers={"X-MAL-CLIENT-ID": mal_id})

    print("MAL response code: %i" % (response.status_code))

    if response.status_code != 200:
        print("Unexpected response code!")
        sys.exit(2)

    query_result = response.json()

    if not query_result["data"]:
        print("MAL query returned nothing!")
        sys.exit(1)

    matching_id = match_titles(
        query_result, guessit_match["title"], title_threshold
    )

    if matching_id:
        open_mal_page(matching_id)
        sys.exit(0)
    else:
        print("No exact match found!")
        sys.exit(3)


def match_titles(mal_response: dict, title_to_match, title_threshold):
    result = mal_response
    nodes = [nodes["node"] for nodes in result["data"]]
    print("No. query results: %i" % (len(nodes)))
    print("First match title %s" % (nodes[0]["title"]))
    for entry in nodes:
        title_similarity = SM(None, title_to_match, entry["title"]).ratio()

        print(
            "comp. titles: %s <-> %s (%.3f)"
            % (title_to_match, entry["title"], title_similarity)
        )

        if title_similarity >= title_threshold:
            return entry["id"]

        # Checking against alternative titles
        for alt_title in titles_to_list(entry["alternative_titles"]):
            title_similarity = SM(None, title_to_match, alt_title).ratio()
            print(
                "comp. titles: %s <-> %s (%.3f)"
                % (
                    title_to_match,
                    alt_title,
                    title_similarity,
                )
            )
            if title_similarity >= title_threshold:
                return entry["id"]
    return None


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
