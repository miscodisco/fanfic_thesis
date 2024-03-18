import json
import time

from tqdm import tqdm
from unidecode import unidecode

from utils import *


def main():
    links = read_lines("new_links.txt")

    works = []
    for link in tqdm(links):
        # checking if it is a works link
        if "/users/" in link:
            continue

        # setting up the url
        url = (
            "https://archiveofourown.org"
            + link.strip()
            + "?view_adult=true"
            + "&amp;view_full_work=true"
        )

        # get soup
        soup = get_soup(url)

        # some fanfics are only for users that are logged in, we skip those
        try:
            title = soup.find("h2").text.strip()
        except AttributeError:
            continue

        # sometimes the url is wrong 
        if title == "Error 404":
            continue


        # save the meta data
        try: 
            data = {
                "url": url.strip(),
                "work_id": link.replace("/works/", "").strip(),
                "title": unidecode(title),
                "author": unidecode(soup.select_one("h3.byline.heading").get_text().strip()),
            }
        except AttributeError:
            print("attribute error, sleeping and trying again")
            soup = get_soup(url)
            time.sleep(300)
            data = {
                "url": url.strip(),
                "work_id": link.replace("/works/", "").strip(),
                "title": unidecode(title),
                "author": unidecode(soup.select_one("h3.byline.heading").get_text().strip()),
            }


        for meta in ["published", "chapters", "words"]:
            data[meta] = soup.select_one(f"dd.{meta}").get_text().replace(",", "")

        for stat in ["kudos", "bookmarks", "comments", "hits"]:
            data[stat] = get_stat(soup, stat)

        for tag in ["fandom", "relationship", "character", "freeform", "rating"]:
            data[tag] = get_tags(soup, tag)

        # get the full text
        text = get_chaptertext(soup)

        # save the text
        data["text"] = text

        # append to the rest
        works.append(data)

        with open("temp2.ndjson", "a") as file:
            file.write(json.dumps(data))
            file.write('\n')

    # save_ndjson('full.ndjson', works)


if __name__ == "__main__":
    main()
