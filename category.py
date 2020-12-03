#! /usr/bin/env python3
# coding: utf-8

''' The purpose of this module is to handle the category
    level methods and functions when scraping content from
    http://books.toscrape.com/ website.
'''

import csv
import os.path
from urllib.parse import urljoin

from book import Book
from utils import connect_with_bs4, progress_monitor, FileIO


##################################################
# Category
##################################################


class Category:
    """ The purpose of this class is to collect
        and store the category information

    Attributes
    ----------
    category_url : str
    name : str
    book_list : list
    links : list
    num_books : int

    Methods
    -------
    collect()
        connect to the given url and collect the product data
    to_csv(path='demo', mode='a')
        write the content of the collected books in the given CSV
    """

    def __init__(self, url=None):
        self.category_url = url
        self.name = None
        self.book_list = []
        self.links = []
        self.num_books = 0

        if url is not None:
            self.collect()

    def collect(self):
        """ Connect to the category page and grab the information """

        self._soup = connect_with_bs4(self.category_url)

        self.name = self.__scrap_name()
        self.num_books = self.__scrap_num_books()
        self.links = self.__scrap_links()
        self.books = self.__scrap_books()

    def to_csv(self, path='demo', mode='a'):
        """ OBSOLETE -> FileIO
            Write the collected books information to a given CSV file
            Append if the file already exists

        Parameters
        ----------
        path : str (default is 'demo')
            The path including its name but without the extension to the csv
        mode : str (default is 'a')
            The file mode used to open the file (r,r+,w,w+,a,a+,x,x+)
        """

        if self.books == []:
            self.collect()

        addHeaders = False
        if not os.path.exists(f'{path}.csv') or (mode != 'a' and mode != 'a+'):
            addHeaders = True

        with open(f"{path}.csv", mode, newline='') as csvfile:

            fields = self.books[0].get_headers()
            writer = csv.DictWriter(csvfile, fieldnames=fields)

            if addHeaders:
                headers = {fields[i]: fields[i] for i in range(len(fields))}
                writer.writerow(headers)

            for book in self.books:
                writer.writerow(book.to_dict())

    def write_csv(self, path=None, mode='a'):
        """ Write the collected books information to a given CSV file
            Append if the file already exists

        Parameters
        ----------
        path : str (default is the category_name)
            The path including the file name (without the extension to the csv)
        mode : str (default is 'a')
            The file mode used to open the file (r,r+,w,w+,a,a+,x,x+)
        """

        if self.books == []:
            self.collect()

        if path is None:
            path = self.name.lower().replace(' ', '_')

        fields = self.books[0].get_headers()
        headers = {fields[i]: fields[i] for i in range(len(fields))}

        if not os.path.exists(f'{path}.csv') or (mode != 'a' and mode != 'a+'):
            FileIO.write(path, fields, headers, mode)

        for book in self.books:
            FileIO.write(path, fields, book.to_dict(), 'a')

    # --- PRIVATE METHODS ---

    def __scrap_name(self):
        try:
            return self._soup.find('h1').string
        except Exception:
            return ''

    def __scrap_num_books(self):
        try:
            return int(self._soup.find('form', class_='form-horizontal')
                                 .find('strong').string)
        except Exception:
            return 0

    def __scrap_links(self):
        def get_links(soup): return soup.select('section a[title]')

        try:
            links = get_links(self._soup)

            page = 2
            while(len(links) < self.num_books):
                base = urljoin(self.category_url, 'page-{}.html'.format(page))
                soup = connect_with_bs4(base)
                links.extend(get_links(soup))
                page += 1

            return [(urljoin(self.category_url, x.attrs['href']),
                     x.attrs['title']) for x in links]
        except Exception:
            return []

    def __scrap_books(self):
        books = []
        book = Book(self.links[0][0]).collect()

        FileIO.open_category(self.name)

        for link in self.links:

            progress_monitor.catbooks_update(
                    len(books),
                    self.num_books,
                    link[1])

            book = Book(link[0])
            book.collect()
            books.append(book)

            book.save_image()

        progress_monitor.catbooks_update(
                    len(books),
                    self.num_books,
                    link[1])

        FileIO.close_category()

        return books
