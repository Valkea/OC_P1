#! /usr/bin/env python3
# coding: utf-8

''' The purpose of this module is to scrape the content of
    the http://books.toscrape.com/ website.
'''

from urllib.request import urljoin
import argparse
from os import chdir, mkdir

from book import Book
from category import Category
from utils import progress_monitor, FileIO, log_error

##################################################
# Scraper
##################################################


class Scraper():
    """ The purpose of this class is to collect
        and store the whole books of the website

    Attributes
    ----------
    site_url : str
    categories : list
    links : list
    num_books : int

    Methods
    -------
    collect()
        connect to the given url and collect the data
    """

    def __init__(self, url):
        self.site_url = url
        self.links = []
        self.categories = []
        self.num_books = 0

        if(url is not None):
            self.collect()

    def collect(self):
        """ Connect to the home-page and grab the information """

        self._soup = FileIO.connect_with_bs4(self.site_url)

        self.num_books = self.__scrap_num_books()
        self.links = self.__scrap_links()
        self.categories = self.__scrap_categories()

    # --- PRIVATE METHODS ---

    @log_error
    def __scrap_num_books(self):
        try:
            return int(self._soup.select('form strong')[0].string)
        except Exception as e:
            raise(e)

    @log_error
    def __scrap_links(self):
        try:
            ahrefs = self._soup.select('div[class=side_categories] li ul a')
            base_url = urljoin(self.site_url, '.')
            return [(urljoin(base_url, x.attrs['href']), x.string.strip())
                    for x in ahrefs]
        except Exception as e:
            raise(e)

    @log_error
    def __scrap_categories(self, to_csv=False):

        FileIO.init_root('data', False)
        categories = []

        progress_monitor.allbooks_init(self.num_books, self.site_url)

        for link in self.links:

            progress_monitor.category_update(
                    len(categories),
                    len(self.links),
                    link[1])

            category = Category(link[0])
            categories.append(category)

            FileIO.open_category(category.name)
            category.write_csv()
            FileIO.close_category()

        return categories


##################################################
# Main
##################################################

@log_error
def move_to_path(path):
    path_list = path.split('/')
    for dirname in path_list:
        try:
            mkdir(dirname)
        except Exception:
            pass
        chdir(dirname)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--slide', type=int, help="Hello world")

    args = parser.parse_args()

    if(args.slide == 1):
        # play with Book class
        print("This part runs the product page scraping only.")
        print("You can check the generated files in demo/slide1")

        move_to_path('demo/slide1')

        prod_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
        book = Book(prod_url)
        book.write_csv('OnProductAppend')
        book.collect()
        book.write_csv('OnProductAlone', 'w')
        book.write_csv('OnProductAlone', 'w')
        book.write_csv('OnProductAppend')
        progress_monitor.complete()

    elif(args.slide == 2):
        # play with Category class
        print("This runs the category page scraping (and hence the product pages)'")
        print("You can check the generated files in demo/slide2")

        move_to_path('demo/slide2')

        cat_url = 'http://books.toscrape.com/catalogue/category/books/fiction_10/index.html'
        cat1 = Category(cat_url)
        cat1.write_csv('cat1')
        cat1.write_csv('cat1')
        progress_monitor.complete()

    elif(args.slide == 3):
        # play with Scraper class
        print("This runs the whole website scraping")
        print("You can check the generated files in demo/slide3")

        move_to_path('demo/slide3')

        site_url = 'http://books.toscrape.com'
        site = Scraper(site_url)
        progress_monitor.complete()

    elif(args.slide == 4):
        # play with FileIO class
        print("This scrape an image")
        print("You can check the generated files in demo/slide4")

        move_to_path('demo/slide4')

        image_url = 'http://books.toscrape.com/media/cache/a3/9e/a39e7c5c9fc61c2ae0f81116aa8cbb0e.jpg'
        FileIO.download_image(image_url, 'demo.jpg')

    else:
        # Scrap the website
        site_url = 'http://books.toscrape.com'
        site = Scraper(site_url)
        progress_monitor.complete()
