#! /usr/bin/env python3
# coding: utf-8

''' The purpose of this module is to scrape the content of
    the http://books.toscrape.com/ website.
'''

from book import Book
from category import Category

##################################################
# Site
##################################################


##################################################
# Main
##################################################

if __name__ == '__main__':

    prod_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    book = Book(prod_url)
    book.to_csv('OneProductAppend')
    book.collect()
    book.to_csv('OneProductAlone')
    book.to_csv('OneProductAppend')

    cat_url = 'http://books.toscrape.com/catalogue/category/books/fiction_10/index.html'
    cat1 = Category(cat_url)
    cat1.to_csv("cat1")
    cat1.to_csv("cat1")
