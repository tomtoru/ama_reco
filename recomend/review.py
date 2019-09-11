# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# for set chrome path
import chromedriver_binary


class Review():
    def __init__(self, item_url, headers):
        self.item_url = item_url
        self.headers = headers
        self.aggregation_stars = {}

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


    def get_star(self):
        # get item page html
        res = requests.get(self.item_url, timeout=1, headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # get review from item page
        review_list = soup.find('div', class_='a-section review-views celwidget')

        for review in review_list:
            personal_page_url = review.find('a', class_="a-profile")['href']

            if personal_page_url is not None:
                self.get_star_from_personal_page(urljoin(self.item_url, personal_page_url))

        print("--finish!--")

    def get_star_from_personal_page(self, personal_url):
        # set options
        options = Options()
        options.set_headless(True)
        driver = webdriver.Chrome(chrome_options=options)

        driver.get(personal_url)
        try:
            # wait until drew review block
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-at-card-container")))
        finally:
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, "html.parser")

        review_list = soup.find('div', id='profile-at-card-container')

        if review_list is None:
            return None

        for review in review_list:
            name_element = review.find('div',
                                       class_='a-section profile-at-product-title-container profile-at-product-box-element')
            star_element = review.find('div', class_='a-row a-spacing-mini')

            if name_element is not None and star_element is not None:
                name = name_element.find('span').find('span').string
                star = star_element.find('span', class_='a-icon-alt').string
                # star: 「星5つのうち{int or float}」
                star_float = float(re.findall('[0-9]|[0-9]+\.[0-9]', star)[1])
                if name in self.aggregation_stars:
                    self.aggregation_stars[name] += star_float
                else:
                    self.aggregation_stars[name] = star_float
