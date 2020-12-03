#! /usr/bin/env python3
# coding: utf-8

''' The purpose of this module is to gather
    the generic functions
'''

from os import get_terminal_size, chdir, mkdir, getcwd
from shutil import rmtree
from urllib.request import urlopen
import csv

from bs4 import BeautifulSoup

##################################################
# Connexion
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
# Progress
##################################################


class Progress():
    """ The purpose of this class is to display the current
        status of the website scraping

    Attributes
    ----------
    _categories : dict
        Overall categories progress informations
    _catbooks : dict
        Current category books progress informations
    _allbooks : dict
        Overall books progress informations

    Methods
    -------
    catbooks_update(current, total, label)
        update the current category scraping progress
    category_update(current, total, label):
        update the  overall categories scraping progress
    allbooks_init(total, label)
        initilize the overall scraping informations
    """

    def __init__(self):
        self._categories = {'current': 0, 'total': 0, 'label': ''}
        self._catbooks = {'current': 0, 'total': 0, 'label': ''}
        self._allbooks = {'current': 0, 'total': 0, 'label': ''}

    def catbooks_update(self, current, total, label):
        self._catbooks = {
                            'current': int(current),
                            'total': int(total),
                            'label': label,
                        }

        if(current != 0):
            self._allbooks['current'] += 1

        self.__update_display()

    def category_update(self, current, total, label):
        self._categories = {
                            'current': int(current),
                            'total': int(total),
                            'label': label,
                          }

        self.__update_display()

    def allbooks_init(self, total, label):
        self._allbooks = {
                            'current': 0,
                            'total': int(total),
                            'label': label,
                        }

    # --- PRIVATE METHODS ---

    def __update_display(self):

        terminal_size = get_terminal_size()
        bar_size = terminal_size.columns - 20
        num_lines = 5

        # Clean terminal
        print(" "*terminal_size.columns*num_lines)
        print("\033[A"*(num_lines+1))

        # Display
        allbooks = self._allbooks
        all_bar = self.__get_progressbar(allbooks, bar_size)
        print(f"{allbooks['label'].center(bar_size)[:bar_size]}")
        print(f"{all_bar} {allbooks['current']}/{allbooks['total']} books")

        cat = self._categories
        # cat_bar = self.__get_progressbar(cat, bar_size)
        # print(f"{cat_bar} {cat['current']}/{cat['total']} categories")
        catlabel = f"Current category: {cat['label']}  "\
                   f"[{cat['current']+1}/{cat['total']}]"
        print(f"{catlabel.center(bar_size)[:bar_size]}")

        catbooks = self._catbooks
        catb_bar = self.__get_progressbar(catbooks, bar_size)
        print(f"{catb_bar} {catbooks['current']}/{catbooks['total']} books")
        print(f"{catbooks['label'].center(bar_size)[:bar_size]}", end='\r')

        # Reset cursor position in terminal
        print("\033[A"*num_lines)

    def __get_progressbar(self, source, bar_size):

        todo_char = '◻'
        done_char = '◼'

        try:
            size = round(bar_size / source['total'] * source['current'])
        except ZeroDivisionError:
            size = 0

        fillchars = done_char*size
        return f"{fillchars.ljust(bar_size,todo_char)}"


progress_monitor = Progress()


##################################################
# Files Inpout / Output
##################################################

CURRENT_WORKING_DIRECTORY = getcwd()


class FileIO:
    """ The purpose of this class is to save the collected
        data to the local storage

    Static Methods
    -------
    init_root(root)
        remove and re-create (if needed) the <root> folder and enter in it
        use it only once !
    open_category(name)
        create the <name> folder and enter into it
    close_category()
        move to the parent folder
    write(path, fields, data, mode)
        write the given data the the given path.csv
    """

    @staticmethod
    def init_root(root):
        """ remove and re-create (if needed) the <root> folder and enter in it
        """
        chdir(CURRENT_WORKING_DIRECTORY)

        try:
            rmtree(root)
        except Exception as e:
            print("FileIO ERROR:", e)

        try:
            mkdir(root)
        except Exception as e:
            print("FileIO ERROR:", e)

        chdir(root)

    @staticmethod
    def open_category(name):
        """ create the <name> folder and enter into it """
        try:
            mkdir(name)
            chdir(name)
        except Exception as e:
            print("FileIO ERROR:", e)

    @staticmethod
    def write(path, fields, data, mode='a'):
        """ Write the collected books information to a given CSV file
            Append if the file already exists

        Parameters
        ----------
        path : str (default is 'demo')
            The path including its name but without the extension to the csv
        fields : dict
            The columns identifiers
        data : dict
            The data to write in each column
        mode : str (default is 'a')
            The file mode used to open the file (r,r+,w,w+,a,a+,x,x+)
        """

        with open(f"{path}.csv", mode, newline='') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writerow(data)

    @staticmethod
    def close_category():
        """ move to the parent folder """
        chdir('..')
