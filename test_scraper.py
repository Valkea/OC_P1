#! /usr/bin/env python3
# coding: utf-8

'''
The purpose of this module is to test the scrape.py scraping module
'''

import pytest
import os.path
import csv

from bs4 import BeautifulSoup

from scraper import Book, connect_with_bs4


##################################################
# Generic
##################################################

def test_connect_with_bs4_TYPE():
    url = 'http://books.toscrape.com'
    assert type(connect_with_bs4(url)) == BeautifulSoup


def test_connect_with_bs4_ERROR():

    with pytest.raises(Exception):
        connect_with_bs4('http://www.xxxfakexxx.xxx')


##################################################
# Book
##################################################

class TestBook():

    def setup_method(self):
        fake_url = 'http://www.fake.url'
        self.book1 = Book(fake_url)

        prod_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
        self.book2 = Book(prod_url)
        self.book2.collect()

        prod_url = 'http://books.toscrape.com/catalogue/soumission_998/index.html'
        self.book3 = Book(prod_url)

    def test_empty_init(self):
        with pytest.raises(Exception):
            Book()

    # --- Getters & Setters ---

    def test_product_page_url(self):
        self.book1.product_page_url = "fake-url"
        assert self.book1.product_page_url == "fake-url"

    def test_universal_product_code(self):
        self.book1.universal_product_code = "fake-upc"
        assert self.book1.universal_product_code == "fake-upc"

    def test_title(self):
        self.book1.title = "fake-title"
        assert self.book1.title == "fake-title"

    def test_price_including_tax(self):
        self.book1.price_including_tax = 42.42
        assert self.book1.price_including_tax == 42.42

    def test_price_excluding_tax(self):
        self.book1.price_excluding_tax = 41.41
        assert self.book1.price_excluding_tax == 41.41

    def test_number_available(self):
        self.book1.number_available = 40
        assert self.book1.number_available == 40

    def test_product_description(self):
        self.book1.product_description = "fake-desc"
        assert self.book1.product_description == "fake-desc"

    def test_category(self):
        self.book1.category = "fake-cat"
        assert self.book1.category == "fake-cat"

    def test_review_rating(self):
        self.book1.review_rating = 10
        assert self.book1.review_rating == 10

    def test_image_url(self):
        self.book1.image_url = "fake-img-url"
        assert self.book1.image_url == "fake-img-url"

    # --- Collect data ---

    def test_parse_product_infos(self):
        url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        assert self.book2.product_page_url == url

    def test_parse_universal_product_code(self):
        assert self.book2.universal_product_code == "a897fe39b1053632"

    def test_parse_title(self):
        assert self.book2.title == "A Light in the Attic"

    def test_parse_price_including_tax(self):
        assert self.book2.price_including_tax == "£51.77"

    def test_parse_price_excluding_tax(self):
        assert self.book2.price_excluding_tax == "£51.77"

    def test_parse_number_available(self):
        assert self.book2.number_available == 22

    def test_parse_product_description(self):
        assert self.book2.product_description == '''It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love th It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love that Silverstein. Need proof of his genius? RockabyeRockabye baby, in the treetopDon't you know a treetopIs no safe place to rock?And who put you up there,And your cradle, too?Baby, I think someone down here'sGot it in for you. Shel, you never sounded so good. ...more'''

    def test_parse_category(self):
        assert self.book2.category == "Poetry"

    def test_parse_review_rating(self):
        assert self.book2.review_rating == 3

    def test_parse_image_url(self):
        url = "http://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg"
        assert self.book2.image_url == url

    # --- CSV ---

    def test_to_dict(self):
        assert isinstance(self.book1.to_dict(), type(dict())) is True

    def test_to_dict_content(self):
        dbook = self.book2.to_dict()
        dbook_keys = dbook.keys()

        assert 'product_page_url' in dbook_keys
        assert 'universal_product_code' in dbook_keys
        assert 'title' in dbook_keys
        assert 'price_including_tax' in dbook_keys
        assert 'price_excluding_tax' in dbook_keys
        assert 'number_available' in dbook_keys
        assert 'product_description' in dbook_keys
        assert 'category' in dbook_keys
        assert 'review_rating' in dbook_keys
        assert 'image_url' in dbook_keys
        assert 'image_local' in dbook_keys
        assert len(dbook_keys) == 11

    def test_get_headers(self):
        headers = self.book2.get_headers()

        assert 'product_page_url' in headers
        assert 'universal_product_code' in headers
        assert 'title' in headers
        assert 'price_including_tax' in headers
        assert 'price_excluding_tax' in headers
        assert 'number_available' in headers
        assert 'product_description' in headers
        assert 'category' in headers
        assert 'review_rating' in headers
        assert 'image_url' in headers
        assert 'image_local' in headers
        assert len(headers) == 11

        print(len(headers), headers)

    def test_to_csv_CREATE_not_collected(self):
        file = 'test'
        self.book3.to_csv(file, 'w')
        assert os.path.exists(f'{file}.csv') is True

        with open(f'{file}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            assert sum(1 for _ in reader) == 2

        os.remove(f'{file}.csv')

    def test_to_csv_CREATE_collected(self):
        file = 'test'
        self.book2.to_csv(file, 'w')
        assert os.path.exists(f'{file}.csv') is True

        with open(f'{file}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            assert sum(1 for _ in reader) == 2

        os.remove(f'{file}.csv')

    def test_to_csv_APPEND(self):
        file = 'test'
        self.book2.to_csv(file, 'w')
        self.book3.to_csv(file)
        self.book3.to_csv(file)

        with open(f'{file}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            assert sum(1 for _ in reader) == 4

        os.remove(f'{file}.csv')

    def test_to_csv_CREATE_new_file(self):
        file = 'test'
        self.book2.to_csv(file)
        self.book3.to_csv(file)
        self.book3.to_csv(file, 'w')

        with open(f'{file}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            assert sum(1 for _ in reader) == 2

        os.remove(f'{file}.csv')


##################################################
# Category
##################################################


##################################################
# Site
##################################################
