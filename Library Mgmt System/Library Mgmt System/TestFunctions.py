# -*- coding: utf-8 -*-
from User import Member, Librarian
from Catalog import Catalog

#creating useres
user1 = Member("prasanna","bangalore",22,"zxcc8765","std123")
user2 = Member("prashanth","bangalore",23,"zxcc5765","std143")

#creating a librarian
lib1 = Librarian("admin","mysore",34,"avcgh4352","emp123")

#adding book and book items
book = lib1.addBook("harry potter","william",2001,500)
lib1.addBookItem(book,"123zxc43","h101")
lib1.addBookItem(book,"123zxc44","h102")
lib1.addBookItem(book,"123zxc45","h103")
lib1.addBookItem(book,"123zxc46","h104")

book = lib1.addBook("ironman","jhon",2005,300)
lib1.addBookItem(book,"125zgc10","g101")
lib1.addBookItem(book,"125zgc11","g102")
lib1.addBookItem(book,"125zgc12","g103")
lib1.addBookItem(book,"125zgc13","g104")

book = lib1.addBook("attitude","xyz",2016,350)
lib1.addBookItem(book,"765zgc10","h101")
lib1.addBookItem(book,"765zgc12","s102")

lib1.displayBooks()#displaying the inventory
print("\n\n")

#issuing the books
user1.issueBook("ironman")
user2.issueBook("attitude")
user1.issueBook("harry potter")
print("books inventory after issued by members")
lib1.displayBooks()
print("\n\n")

#returning the books
print("books inventry after returning the books by user1 and user2")
user1.returnBook("harry potter")
user2.returnBook("attitude")
lib1.displayBooks()



