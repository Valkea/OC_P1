#! /usr/bin/env python3
# coding: utf-8

'''
The purpose of this module is to test the Scrap class
'''

from scraper import Scraper
from category import Category

##################################################
# Scraper
##################################################


class TestScraper:

    @classmethod
    def setup_class(cls):
        url = 'http://books.toscrape.com/index.html'
        cls.site1 = Scraper(None)
        cls.site2 = Scraper(url)

    # --- Incoming Getters & Setters ---

    def test_url(self):
        self.site1.site_url = "fake-url"
        assert self.site1.site_url == "fake-url"

    def test_links(self):
        self.site1.links = ['url1', 'url2']
        assert self.site1.links == ['url1', 'url2']

    def test_categories(self):
        category1, category2 = Category(None), Category(None)
        self.site1.categories = [category1, category2]
        assert self.site1.categories == [category1, category2]

    def test_num_books(self):
        self.site1.num_books = 42
        assert self.site1.num_books == 42

    # --- Collect data ---

    # def test_parse_category_infos(self):
    #    url = "http://books.toscrape.com/index.html"
    #    assert self.site2.product_page_url == url

    def test_parse_num_books(self):
        assert self.site2.num_books == 1000

    def test_parse_links(self):
        link0 = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
        link10 = "http://books.toscrape.com/catalogue/category/books/religion_12/index.html"
        link20 = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
        link49 = "http://books.toscrape.com/catalogue/category/books/crime_51/index.html"

        assert self.site2.links[0] == (link0, 'Travel')
        assert self.site2.links[10] == (link10, 'Religion')
        assert self.site2.links[20] == (link20, 'Science')
        assert self.site2.links[49] == (link49, 'Crime')
        assert len(self.site2.links) == 50

    def test_parse_categories(self):
        assert self.site2.categories[0].num_books == 11
        assert self.site2.categories[1].num_books == 32
        assert self.site2.categories[10].num_books == 7
        assert self.site2.categories[49].num_books == 1
