import sys
import requests
from bs4 import BeautifulSoup


URL = sys.argv[1]
headers = {"User-Agent": "test"}

if __name__ == "__main__":

    res = requests.get(URL, timeout=1, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    elem_list = soup.find('div', class_="a-section review-views celwidget")


    for elem in elem_list:
        # print(type(elem))
        # print(elem)
        review = elem.select('span.a-icon-alt')
        print(review)
        if review is not None:
            print(review)
