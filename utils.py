#! /usr/bin/env python3
# coding: utf-8

''' The purpose of this module is to gather
    the generic functions
'''

from os import get_terminal_size
from urllib.request import urlopen

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
