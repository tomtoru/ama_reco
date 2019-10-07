# -*- coding: utf-8 -*-

import unittest
from recomend.review import Review

import logging


class TestReview(unittest.TestCase):
    # TODO improve logging
    logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        # TODO
        self.url = "https://www.amazon.co.jp/Python%E3%81%AB%E3%82%88%E3%82%8BWeb%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0-Ryan-Mitchell/dp/4873117615/test/test?test=test"
        self.header = {"User-Agent": "test"}

    def test_run(self):
        # TODO set expected
        # expected =
        model = Review(self.url, self.header)
        result = model.get_star()
        # self.assertEqual(expected, result)
        print(model.aggregation_stars)


if __name__ == "__main__":
    unittest.main()
