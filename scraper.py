#! /usr/bin/env python3
# coding: utf-8

''' The purpose of this module is to scrape the content of
    the http://books.toscrape.com/ website.
'''

import re
from urllib.request import urlopen
from urllib.parse import urljoin

from bs4 import BeautifulSoup


##################################################
# Generic
##################################################


def connect_with_bs4(url):
    """ Connect to the given URL, collect the html data
        and return a BeautifulSoup object to work with

    Parameters
    ----------
    url : str
        The internet address to use in order to collect the data

    Returns
    -------
    BeautifulSoup
        An object containing parsed html data
    """

    page = urlopen(url)
    html = page.read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')

    return soup

##################################################
# Book
##################################################


class Book():
    """ The purpose of this class is to collect
        and store the product information
    """

    def __init__(self, url):
        """
        Parameters
        ----------
        url : str
            The internet address of the product page
        """

        self.product_page_url = url
        self.universal_product_code = None
        self.title = None
        self.price_including_tax = None
        self.price_excluding_tax = None
        self.number_available = None
        self.product_description = None
        self.category = None
        self.review_rating = None
        self.image_url = None

    def collect(self):
        """ Connect to the product page and grab the information """

        self.soup = connect_with_bs4(self.product_page_url)

        self.universal_product_code = self.__scrap_upc()
        self.title = self.__scrap_title()
        self.price_including_tax = self.__scrap_price_inc_tax()
        self.price_excluding_tax = self.__scrap_price_exc_tax()
        self.number_available = self.__scrap_number_available()
        self.product_description = self.__scrap_product_description()
        self.category = self.__scrap_category()
        self.review_rating = self.__scrap_review_rating()
        self.image_url = self.__scrap_image_url()

    def __scrap_upc(self):
        try:
            return self.soup.find('th', string='UPC').find_next('td').string
        except Exception:
            return ''

    def __scrap_title(self):
        try:
            return self.soup.find('h1').string
        except Exception:
            return ''

    def __scrap_price_inc_tax(self):
        try:
            return self.soup.find('th', string="Price (incl. tax)") \
                            .find_next('td').string
        except Exception:
            return ''

    def __scrap_price_exc_tax(self):
        try:
            return self.soup.find('th', string="Price (excl. tax)") \
                            .find_next('td').string
        except Exception:
            return ''

    def __scrap_number_available(self):
        try:
            number_available_txt = self.soup.find('th', string='Availability')\
                                            .find_next('td').string

            return int(re.search(r'[0-9]+', number_available_txt).group())
        except Exception:
            return ''

    def __scrap_product_description(self):
        try:
            return self.soup.select("#product_description")[0]  \
                            .find_next('p').string
        except Exception:
            return ''

    def __scrap_category(self):
        try:
            return self.soup.find('ul', class_='breadcrumb')    \
                            .findAll('a')[2].string
        except Exception:
            return ''

    def __scrap_review_rating(self):
        try:
            trans = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            return trans[(
                self.soup.find('p', class_='star-rating')
                .attrs['class'][1])]
        except Exception:
            return ''

    def __scrap_image_url(self):
        try:
            relative_url = self.soup.img.attrs['src']  # relative
            base_url = urljoin(self.product_page_url, '.')
            return urljoin(base_url, relative_url)  # absolute
        except Exception as e:
            return e


prod_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
book = Book(prod_url)
book.collect()

##################################################
# Category
##################################################


##################################################
# Site
##################################################
