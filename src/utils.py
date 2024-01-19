import json
import re
import time

from bs4 import BeautifulSoup
import lxml
import requests
from unidecode import unidecode


def read_lines(filename):
    """
    read the links in a file
    """
    with open(filename, "r") as f:
        lines = f.readlines()

    return lines


def get_soup(url):
    """
    get the beautiful soup from a url
    from the Ao3 scraper: https://github.com/radiolarian/AO3Scraper/tree/master
    """
    page = requests.get(url)
    status = page.status_code

    while status == 429:
        print("Request answered with Status-Code 429")
        print("Trying again in 1 minute...")
        time.sleep(60)
        page = requests.get(url)
        status = page.status_code

    time.sleep(5)

    soup = BeautifulSoup(page.text, "lxml")

    return soup


def get_links(soup):
    """
    retrives links to works on a search page on AO3
    """
    works = soup.select("h4 a")
    links = []
    for work in works:
        if "/works/" in work.get("href"):
            links.append(work.get("href"))

    return links


def get_stat(soup, stat):
    """
    returns the number for the given stat. if the stat does not exist, None is returned
    """
    try:
        result = int(soup.select_one(f"dd.{stat}").get_text().replace(",", ""))
    except AttributeError:
        result = 0

    return result


def get_tags(soup, tag):
    """
    returns a list of tags for a given tag type 
    """
    css_pattern = f"dd.{tag}.tags > ul.commas > li"

    tags_list = [unidecode(element.get_text()) for element in soup.select(css_pattern)]

    return tags_list


def get_chaptertext(soup):
    """
    from the Ao3 scraper: https://github.com/radiolarian/AO3Scraper/tree/master 
    """
    chapters = soup.select("div#chapters p")

    text = "\n\n".join([unidecode(chapter.text) for chapter in chapters])
    return text


def save_ndjson(filename:str, works):
    with open(filename, "w", encoding="UTF-8") as f:
        for work in works:
            f.write(json.dumps(work))
            f.write("\n")