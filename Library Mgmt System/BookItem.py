# -*- coding: utf-8 -*-
class BookItem:
    def __init__(self,book,isbn,rack):
        self.book = book
        self.isbn = isbn
        self.rack = rack
        self.status = 0
        self.member = None
        self.duetime = 0
        self.total_issued_time = 0
        
