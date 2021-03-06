# -*- coding: utf-8 -*-
from Book import Book
#First Book is file & second is Class

class Catalog:
    def __init__(self):
        self.different_book_count = 0
        self.books = []
        
    #Only available to admin
    def addBook(self,name,author,publish_date,pages):
        b = Book(name,author,publish_date,pages)
        self.different_book_count += 1
        self.books.append(b)
        return b
    
    #Only available to admin
    def addBookItem(self,book,isbn,rack):
        book.addBookItem(isbn, rack)
        
    def searchByName(self,name):
        for book in self.books:
            if name == book.name:
                return book
                break
    
    def searchByAuthor(self,author):
        for book in self.books:
            if author == book.author:
                return True
                break

    
        
    def displayAllBooks(self):
        print("**************Welcome to Library Management System**************")

        print ('Different Book Count',self.different_book_count)
        c = 0
        print("{}\t{}\t{}\t{}\t{}".format("Book Name","Author","Total Books","Books issued","Books Available"))
        for book in self.books:
            book.printBook()
