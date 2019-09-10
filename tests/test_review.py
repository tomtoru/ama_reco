# -*- coding: utf-8 -*-

import unittest
from recomend.review import Review

class TestReview(unittest.TestCase):

    def setUp(self):
        # TODO
        self.url = "https://www.amazon.co.jp/Python%E3%81%AB%E3%82%88%E3%82%8BWeb%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0-%E7%AC%AC2%E7%89%88-Ryan-Mitchell/dp/4873118719"
        self.header = {"User-Agent": "test"}


    def test_run(self):
        # TODO set expected
        # expected =
        model = Review(self.url, self.header)
        result = model.get_star()
        # self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()