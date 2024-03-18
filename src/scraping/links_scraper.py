import json
import re
import time

from tqdm import tqdm
from bs4 import BeautifulSoup
import lxml
import requests

from utils import read_lines, get_soup, get_links


def main():
    urls = read_lines("urls.txt")

    all_links = []

    for url in urls:
        print(url)
        soup = get_soup(url)

        # pattern for the total number of pages
        pattern = r"(\d+) N"
        n_pages = re.search(
            pattern, soup.select_one("ol.pagination.actions").get_text()
        ).group(1)

        links = []

        for i in tqdm(range(1,int(n_pages) + 1)):
            # if it's the first page we don't need to update the soup
            if i == 1:
                links.extend(get_links(soup))
            else:
                temp_links = []
                # update url
                page_pattern = r"page\=\d+"
                url = re.sub(page_pattern, "page=" + str(i), url)

                # get new soup and fedge links
                pagesoup = get_soup(url)
                temp_links = get_links(pagesoup)

                while temp_links == []:
                    print("links no work, sleeping a min, trying again")
                    time.sleep(60)
                    pagesoup = get_soup(url)
                    temp_links = get_links(pagesoup)

                # saving the links for this page 
                links.extend(temp_links)

                
        # saving the links for this url to all links
        all_links.extend(links)

        # save all links so far in a file, no reason to wait til the end in case of errors 
        with open("new_links.txt", "w") as f:
            f.write('\n'.join(all_links))


if __name__ == "__main__":
    main()
