# -*- coding: utf-8 -*-
import time
from Catalog import Catalog

catalog = Catalog()


class User:
    def __init__(self, name, location, age, aadhar_id):
        self.name = name
        self.location = location
        self.age = age
        self.aadhar_id = aadhar_id
        

class Member(User):
    def __init__(self,name, location, age, aadhar_id,student_id):
        super().__init__(name, location, age, aadhar_id)
        self.student_id = student_id
        
    def __repr__(self):
        return self.name + ' ' + self.location + ' ' + self.student_id
    
    #assume name is unique
    def issueBook(self,name,days=10):
        for book in catalog.books:
            if name == book.name:
                for book_item in book.book_item:
                    if book_item.status == 0:
                        book_item.status == 1
                        book_item.member = self
                        book_item.duetime = days*60
                        book_item.total_issued_time = time.time()
                        return book_item
                        break
        
    
    #assume name is unique
    def returnBook(self,name):
        end = time.time()
        for book in catalog.books:
            if name == book.name:
                for book_item in book.book_item:
                    if book_item.Member == self:
                        total_time = end - book_item.total_issued_time
                        if book_item.duetime < int(total_time):
                            pass
                        book_item.status = 0
                        book_item.member = None
                        book_item.duetime = 0
                        book_item.total_issued_time = 0


        
        
class Librarian(User):
    
    def __init__(self,name, location, age, aadhar_id,emp_id):
        super().__init__(name, location, age, aadhar_id)
        self.emp_id = emp_id
        
    def __repr__(self):
        return self.name + self.location + self.emp_id
    
    def addBook(self,name,author,publish_date,pages):
        book = catalog.addBook(name,author,publish_date,pages)
        return book
    
    def addBookItem(self,book,isbn,rack):
        catalog.addBookItem(book,isbn,rack)

    
    def removeBook(self,name):
        for book in catalog.books:
            if name == book.name:
                catalog.books.remove(book)
                return True
                break

    
    
        