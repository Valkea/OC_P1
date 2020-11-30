#! /usr/bin/env python3
# coding: utf-8

'''
The purpose of this module is to scrape the content 
of the http://books.toscrape.com/ website.
'''

##################################################
### Book
##################################################

class Book():

    def __init__(self, url):
        self.Iproduct_page_url = url
        self.Iuniversal_product_code = None
        self.Ititle = None
        self.Iprice_including_tax = None
        self.Iprice_excluding_tax = None
        self.Inumber_available = None
        self.Iproduct_description = None
        self.Icategory = None
        self.Ireview_rating = None
        self.Iimage_url = None

##################################################
### Category
##################################################


##################################################
### Site
##################################################
