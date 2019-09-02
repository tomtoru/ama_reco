import sys
import requests
from bs4 import BeautifulSoup
import re


def get_star(url, headers):
    res = requests.get(url, timeout=1, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    elem_list = soup.find('div', class_="a-section review-views celwidget")

    star_list = []
    for elem in elem_list:
        review = elem.select('span.a-icon-alt')
        if review is not None:
            star = float(re.findall('[0-9]+\.[0-9]', review[0].text)[0])
            star_list.append(star)

    star_count = 0.0
    for s in star_list:
        star_count += s

    return star_count

def clawl_review():
    pass

def count_stars():
    pass


if __name__ == "__main__":
    url = sys.argv[1]
    headers = {"User-Agent": "test"}

    stars = get_star(url, headers)
    print(stars)

