#! /usr/bin/env python3
# coding: utf-8

''' The purpose of this module is to scrape the content of
    the http://books.toscrape.com/ website.
'''

import re
import csv
import os
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

        Attributes
        ----------
        product_page_url : str
        universal_product_code : str
        title : str
        price_including_tax : str
        price_excluding_tax : str
        number_available : str
        product_description : str
        category : str
        review_rating : int
        image_url : str
        image_local : str

        Methods
        -------
        get_headers()
            return a list of the attributes names to use in the CSV
        to_dict()
            return a dict of the attributes and values to use in the CSV
        collect()
            connect to the given url and collect the product data
        to_csv(path='demo', mode='a')
            write the content of this instance in the given CSV 
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
        self.image_local = None

    def get_headers(self):
        """ Return a list containing the appropriate headers for the CSV export

        Returns
        -------
        list:
            The list of the selected attributes names
        """
        return [h for h in self.__dict__.keys() if not h.startswith('_')]

    def to_dict(self):
        """ Return a dictionary containing the appropriate key/value
            pairs for the CSV export

        Returns
        -------
        dict:
            The dict of the selected attributes names along with their values
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def collect(self):
        """ Connect to the product page and grab the information """

        self._soup = connect_with_bs4(self.product_page_url)

        self.universal_product_code = self.__scrap_upc()
        self.title = self.__scrap_title()
        self.price_including_tax = self.__scrap_price_inc_tax()
        self.price_excluding_tax = self.__scrap_price_exc_tax()
        self.number_available = self.__scrap_number_available()
        self.product_description = self.__scrap_product_description()
        self.category = self.__scrap_category()
        self.review_rating = self.__scrap_review_rating()
        self.image_url = self.__scrap_image_url()

    def to_csv(self, path='demo', mode='a'):
        """ Write the qualified attributes of the Book object to a given CSV file
            Append if the file already exists

        Parameters
        ----------
        path : str (default is 'demo')
            The path including its name but without the extension to the csv file
        mode : str (default is 'a')
            The file mode used to open the file (r,r+,w,w+,a,a+,x,x+)
        """

        if self.title is None:
            self.collect()

        addHeaders = False
        if not os.path.exists(f'{path}.csv') or (mode != 'a' and mode != 'a+'):
            addHeaders = True

        with open(f"{path}.csv", mode, newline='') as csvfile:

            fields = self.get_headers()
            writer = csv.DictWriter(csvfile, fieldnames=fields)

            if addHeaders:
                headers = {fields[i]: fields[i] for i in range(len(fields))}
                writer.writerow(headers)

            writer.writerow(self.to_dict())

    # --- PRIVATE METHODS ---

    def __scrap_upc(self):
        try:
            return self._soup.find('th', string='UPC').find_next('td').string
        except Exception:
            return ''

    def __scrap_title(self):
        try:
            return self._soup.find('h1').string
        except Exception:
            return ''

    def __scrap_price_inc_tax(self):
        try:
            return self._soup.find('th', string="Price (incl. tax)") \
                            .find_next('td').string
        except Exception:
            return ''

    def __scrap_price_exc_tax(self):
        try:
            return self._soup.find('th', string="Price (excl. tax)") \
                            .find_next('td').string
        except Exception:
            return ''

    def __scrap_number_available(self):
        try:
            number_available_txt = self._soup                               \
                                        .find('th', string='Availability')  \
                                        .find_next('td').string

            return int(re.search(r'[0-9]+', number_available_txt).group())
        except Exception:
            return ''

    def __scrap_product_description(self):
        try:
            return self._soup.select("#product_description")[0]  \
                            .find_next('p').string
        except Exception:
            return ''

    def __scrap_category(self):
        try:
            return self._soup.find('ul', class_='breadcrumb')    \
                            .findAll('a')[2].string
        except Exception:
            return ''

    def __scrap_review_rating(self):
        try:
            trans = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            return trans[
                    (self._soup.find('p', class_='star-rating')
                        .attrs['class'][1])]
        except Exception:
            return ''

    def __scrap_image_url(self):
        try:
            relative_url = self._soup.img.attrs['src']  # relative
            base_url = urljoin(self.product_page_url, '.')
            return urljoin(base_url, relative_url)  # absolute
        except Exception as e:
            return e


prod_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
book = Book(prod_url)
book.to_csv('OneProductAppend')
book.collect()
book.to_csv('OneProductAlone')
book.to_csv('OneProductAppend')

##################################################
# Category
##################################################


##################################################
# Site
##################################################
