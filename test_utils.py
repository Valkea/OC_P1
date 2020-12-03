#! /usr/bin/env python3
# coding: utf-8

'''
The purpose of this module is to test the class and methods
defined in utils.py
'''
from os import getcwd, chdir, mkdir, rmdir, remove
from os import path
from urllib.request import urljoin

from utils import FileIO

##################################################
# FileIO
##################################################


class TestFileIO:

    @classmethod
    def setup_class(cls):
        try:
            mkdir('testzone')
        except Exception:
            pass

        chdir('testzone')
        cls.cwd = getcwd()

    @classmethod
    def teardown_class(cls):
        chdir('..')
        try:
            rmdir('testzone')
        except Exception:
            pass

    def test_init_root(self):
        dirname = 'testinit'
        assert getcwd() == self.cwd
        FileIO.init_root(dirname, False)
        assert getcwd() == urljoin(self.cwd+'/', dirname)
        chdir('..')
        assert path.exists(dirname) is True
        rmdir(dirname)

    def test_open_category(self):
        catname = 'testcat'
        FileIO.open_category(catname)
        assert getcwd() == urljoin(self.cwd+'/', catname)
        chdir('..')
        assert path.exists(catname) is True
        rmdir(catname)

    def test_close_category(self):
        dirname = "testclose"
        assert getcwd() == self.cwd
        mkdir(dirname)
        chdir(dirname)
        FileIO.close_category()
        assert getcwd() == self.cwd
        rmdir(dirname)

    def test_write(self):
        filepath = 'testwrite'
        FileIO.write(filepath, ['a'], {'a': 'hello'}, 'w')
        assert path.exists(f"{filepath}.csv") is True
        remove(f"{filepath}.csv")

    def test_download_image(self):
        url = "http://books.toscrape.com/media/cache/c0/59/c05972805aa7201171b8fc71a5b00292.jpg"
        name = "testdownload.jpg"
        FileIO.download_image(url, name)
        assert path.exists(name)
        remove(name)
