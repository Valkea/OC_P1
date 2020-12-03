#! /usr/bin/env python3
# coding: utf-8

'''
The purpose of this module is to test the Category class
'''

import os.path
import csv

from scraper import Book, Category

##################################################
# Category
##################################################


class TestCategory:

    @classmethod
    def setup_class(cls):
        url = 'http://books.toscrape.com/catalogue/category/books/fiction_10/index.html'
        cls.cat1 = Category(None)
        cls.cat2 = Category(url)

    # def test_empty_init(self):
    #    with pytest.raises(Exception):
    #        Category()

    # --- Incoming Getters & Setters ---

    def test_name(self):
        self.cat1.name = "fake-name"
        assert self.cat1.name == "fake-name"

    def test_url(self):
        self.cat1.url = "fake-url"
        assert self.cat1.url == "fake-url"

    def test_books(self):
        book1, book2 = Book('url1'), Book('url2')
        self.cat1.books = [book1, book2]
        assert self.cat1.books == [book1, book2]

    def test_links(self):
        self.cat1.links = ['url1', 'url2']
        assert self.cat1.links == ['url1', 'url2']

    def test_num_books(self):
        self.cat1.num_books = 42
        assert self.cat1.num_books == 42

    # --- Collect data ---

    # def test_parse_category_infos(self):
    #    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    #    assert self.book2.product_page_url == url

    def test_parse_name(self):
        assert self.cat2.name == "Fiction"

    def test_parse_num_books(self):
        assert self.cat2.num_books == 65

    def test_parse_links(self):
        link0 = "http://books.toscrape.com/catalogue/soumission_998/index.html"
        link39 = "http://books.toscrape.com/catalogue/me-before-you-me-before-you-1_434/index.html"
        link64 = "http://books.toscrape.com/catalogue/bright-lines_11/index.html"

        assert self.cat2.links[0][0] == link0
        assert self.cat2.links[39][0] == link39
        assert self.cat2.links[64][0] == link64
        assert len(self.cat2.links) == 65

    def test_parse_books(self):
        title0 = "Soumission"
        upc3 = "709822d0b5bcb7f4"
        availability21 = 14
        rate39 = 1
        assert len(self.cat2.books) == 65
        assert self.cat2.books[0].title == title0
        assert self.cat2.books[3].universal_product_code == upc3
        assert self.cat2.books[21].number_available == availability21
        assert self.cat2.books[39].review_rating == rate39

    # --- CSV ---

    def test_to_csv(self):
        file = 'test-category'
        self.cat2.write_csv(file)

        with open(f'{file}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            assert sum(1 for _ in reader) == 66

        os.remove(f'{file}.csv')

    def test_to_csv_APPEND(self):
        file = 'test-category'
        self.cat2.write_csv(file)
        self.cat2.write_csv(file)

        with open(f'{file}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            assert sum(1 for _ in reader) == 131

        os.remove(f'{file}.csv')

    def test_to_csv_CREATE_new_file(self):
        file = 'test-category'
        self.cat2.write_csv(file)
        self.cat2.write_csv(file)
        self.cat2.write_csv(file, 'w')

        with open(f'{file}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            assert sum(1 for _ in reader) == 66

        os.remove(f'{file}.csv')
