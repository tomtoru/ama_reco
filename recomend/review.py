# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os
import time
import logging
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# for set chrome path
import chromedriver_binary


class Review():
    def __init__(self, item_url, headers, star_filter=4.0):
        # exclude parameter
        self.item_url = re.search(r"https://.+?/.+?/dp/[a-zA-Z0-9]+", item_url).group()
        self.headers = headers
        self.star_filter = star_filter
        self.aggregation_stars = {}
        self.now_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.result_dir = './recomend/result/'

    def get_star(self):
        start = time.time()
        logging.debug(':::::start')

        # get item page html
        res = requests.get(self.item_url, timeout=1, headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # get all review page html
        all_review_url = soup.find("a", attrs={"data-hook": "see-all-reviews-link-foot"}).attrs["href"]
        soup_res_all_review_list = []
        while True:
            res_all_review = requests.get(urljoin(self.item_url, all_review_url), timeout=1, headers=self.headers)
            soup_all_review = BeautifulSoup(res_all_review.text, "html.parser")
            soup_res_all_review_list.append(soup_all_review)

            soup_pagination = soup_all_review.find("ul", class_="a-pagination")
            if soup_pagination is None:
                break
            elif soup_pagination.find("li", class_="a-last") is None:
                break
            elif soup_pagination.find("li", class_="a-last").find("a", recursive=False) is None:
                break
            else:
                all_review_url = soup_pagination.find("li", class_="a-last").find("a", recursive=False)["href"]


        # get review from item page
        for soup_res_all_review in soup_res_all_review_list:
            review_list = soup_res_all_review.find("div", id="cm_cr-review_list")
            logging.debug(':::::get {0} review'.format(len(review_list)))
            for review in review_list:
                # TODO check why sometimes get "None"...?
                if review.find('span', class_='a-icon-alt') is None:
                    continue

                # filter by star count
                star = review.find('span', class_='a-icon-alt').string
                if float(re.findall('[0-9]\.[0-9]', star)[0]) < self.star_filter:
                    continue

                # check reviewer's personal page
                personal_page_url = review.find('a', class_="a-profile")['href']
                if personal_page_url is not None:
                    self.get_star_from_personal_page(urljoin(self.item_url, personal_page_url))

        self.organize_aggregation()

        # result dir check
        if not os.path.isdir(self.result_dir):
            os.makedirs(self.result_dir)
        # detail of result save
        result_log = self.result_dir + 'result_{0}.txt'.format(self.now_datetime)
        with open(result_log, 'w') as f:
            f.write(str(self.aggregation_stars))

        logging.debug(':::::finish')
        logging.debug(':::::time [ {0} ]'.format(time.time() - start))

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
            html = driver.page_source

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            current_html = driver.page_source

            if html == current_html:
                break
            else:
                html = current_html

        soup = BeautifulSoup(html.encode('utf-8'), "html.parser")
        review_list = soup.find('div', id='profile-at-card-container')

        if review_list is None:
            return None

        tmp_aggregation_stars = {}
        duplicate_count = {}
        for review in review_list:
            # TODO: to exclude base item from aggregation
            name_element = review.find('div',
                                       class_='a-section profile-at-product-title-container profile-at-product-box-element')
            star_element = review.find('div', class_='a-row a-spacing-mini')

            if name_element is not None and star_element is not None:
                name = name_element.find('span').find('span').string
                if name is None:
                    # TODO check why sometimes get "None"...?
                    continue
                # exclude volume number for series items
                name = re.sub(r"\d*", "", name)

                star = star_element.find('span', class_='a-icon-alt').string
                # star: 「星5つのうち{int or float}」
                star_float = float(re.findall('[0-9]|[0-9]+\.[0-9]', star)[1])
                if name in tmp_aggregation_stars:
                    tmp_aggregation_stars[name] += star_float
                    duplicate_count[name] += 1
                else:
                    tmp_aggregation_stars[name] = star_float
                    duplicate_count[name] = 1

        for name, star in tmp_aggregation_stars.items():
            if name in self.aggregation_stars:
                self.aggregation_stars[name] += star / float(duplicate_count[name])
            else:
                self.aggregation_stars[name] = star / float(duplicate_count[name])

    def organize_aggregation(self):
        self.aggregation_stars = sorted(self.aggregation_stars.items(), reverse=True, key=lambda x: x[1])
        # TODO: make result for output
