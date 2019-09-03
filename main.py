import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


# def get_star(url, headers):
#     res = requests.get(url, timeout=1, headers=headers)
#     soup = BeautifulSoup(res.text, "html.parser")
#     elem_list = soup.find('div', class_="a-section review-views celwidget")
#
#     star_list = []
#     for elem in elem_list:
#         review = elem.select('span.a-icon-alt')
#         if review is not None:
#             star = float(re.findall('[0-9]+\.[0-9]', review[0].text)[0])
#             star_list.append(star)
#
#     star_count = 0.0
#     for s in star_list:
#         star_count += s
#
#     return star_count


def get_star(url, headers):
    # get item page html
    res = requests.get(url, timeout=1, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # get review from item page
    review_list = soup.find('div', class_='a-section review-views celwidget')

    for review in review_list:
        personal_page_url = review.find('a', class_="a-profile")['href']

        if personal_page_url is not None:
            get_star_from_personal_page(urljoin(url, personal_page_url), headers)

    return None


def get_star_from_personal_page(url, headers):
    res = requests.get(url, timeout=1, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    f = open("./test.log", mode='w')
    f.write(str(soup))
    f.close()
    review_list = soup.find('div', class_='a-section')
    print(review_list)


    if review_list is None:
        return None

    for review in review_list:
        star_and_item_name = review.find('div', class_="a-section profile-at-product-title-container profile-at-product-box-element")

        if star_and_item_name is not None:
            print(star_and_item_name)


def clawl_review():
    pass


def count_stars():
    pass


if __name__ == "__main__":
    url = sys.argv[1]
    headers = {"User-Agent": "test"}

    stars = get_star(url, headers)
    print(stars)

