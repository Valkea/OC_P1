#! /usr/bin/env python3
# coding: utf-8

'''
The purpose of this module is to test the scrape.py scraipping module.
'''

import pytest

from scraper import Book


##################################################
### Generic
##################################################


##################################################
### Book
##################################################

class TestBook():

    def setup_method(self):
        fake_url = 'http://www.fake.url'
        self.book = Book(fake_url)

    def test_prodduct_page_url(self):
        self.book.product_page_url = "fake-url"
        assert self.book.product_page_url == "fake-url"

    def test_universal_product_code(self):
        self.book.universal_product_code = "fake-upc"
        assert self.book.universal_product_code == "fake-upc"

    def test_title(self):
        self.book.title = "fake-title"
        assert self.book.title == "fake-title"

    def test_price_including_tax(self):
        self.book.price_including_tax = 42.42
        assert self.book.price_including_tax == 42.42

    def test_price_excluding_tax(self):
        self.book.price_excluding_tax = 41.41
        assert self.book.price_excluding_tax == 41.41

    def test_number_available(self):
        self.book.number_available = 40
        assert self.book.number_available == 40

    def test_product_description(self):
        self.book.product_description = "fake-desc"
        assert self.book.product_description == "fake-desc"

    def test_category(self):
        self.book.category = "fake-cat"
        assert self.book.category == "fake-cat"

    def test_review_rating(self):
        self.book.review_rating = 10
        assert self.book.review_rating == 10

    def test_image_url(self):
        self.book.image_url = "fake-img-url"
        assert self.book.image_url == "fake-img-url"

                

##################################################
### Category
##################################################


##################################################
### Site
##################################################
