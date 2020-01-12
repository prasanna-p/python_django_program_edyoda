# -*- coding: utf-8 -*-
from BookItem import BookItem

class Book:
    def __init__(self,name,author,publish_date,pages):
        self.name = name
        self.author = author
        self.publish_date = publish_date
        self.pages = pages
        self.total_count = 0
        self.issued_count = 0
        self.book_item = []
        
    def addBookItem(self,isbn,rack):
        b = BookItem(self,isbn,rack)
        self.book_item.append(b)
        self.total_count +=1
        
    def printBook(self):
        available_count = self.total_count - self.issued_count
        print("{:10}\t{:5}\t{:10}\t{:10}\t{:10}".format(self.name,self.author,self.total_count,self.issued_count,available_count))
        