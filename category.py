#! /usr/bin/env python3
# coding: utf-8

''' The purpose of this module is to handle the category
    level methods and functions when scraping content from
    http://books.toscrape.com/ website.
'''

import os.path
from urllib.parse import urljoin

from book import Book
from utils import progress_monitor, FileIO, log_error


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
    auto_collect: bool
        determine if the categories are automatically collected
        when the Category instance is created
    dl_image : bool
        determine if the images are downloaded on local
        drive when scraping the products infos

    Methods
    -------
    collect()
        connect to the given url and collect the product data
    to_csv(path='demo', mode='a')
        write the content of the collected books in the given CSV
    """

    def __init__(self, url=None, auto_collect=True, dl_image=True):
        self.category_url = url
        self.name = None
        self.book_list = []
        self.links = []
        self.num_books = 0
        self.dl_image = dl_image

        if url is not None and auto_collect:
            self.collect()

    def collect(self):
        """ Connect to the category page and grab the information """

        self._soup = FileIO.connect_with_bs4(self.category_url)

        self.name = self.__scrap_name()
        self.num_books = self.__scrap_num_books()
        self.links = self.__scrap_links()
        self.books = self.__scrap_books()

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

    @log_error
    def __scrap_name(self):
        try:
            return self._soup.find('h1').string
        except Exception:
            raise(Exception(f"Can't find the Category name ::\
                    \n{self.product_page_url}"))

    @log_error
    def __scrap_num_books(self):
        try:
            return int(self._soup.find('form', class_='form-horizontal')
                                 .find('strong').string)
        except Exception:
            raise(Exception(f"Can't find the Book number ::\
                    \n{self.product_page_url}"))

    @log_error
    def __scrap_links(self):
        def get_links(soup): return soup.select('section a[title]')

        try:
            links = get_links(self._soup)

            page = 2
            while(len(links) < self.num_books):
                base = urljoin(self.category_url, 'page-{}.html'.format(page))
                soup = FileIO.connect_with_bs4(base)
                links.extend(get_links(soup))
                page += 1

            return [(urljoin(self.category_url, x.attrs['href']),
                     x.attrs['title']) for x in links]
        except Exception:
            raise(Exception(f"Can't find the Book links ::\
                    \n{self.product_page_url}"))

    @log_error
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

            if self.dl_image:
                book.save_image()

        progress_monitor.catbooks_update(
                    len(books),
                    self.num_books,
                    link[1])

        FileIO.close_category()

        return books
