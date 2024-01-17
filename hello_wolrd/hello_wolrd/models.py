import reflex as rx
from datetime import datetime
import sqlmodel

class Author(rx.Model, table=True):
    Authorname: str
    email: str
    birth_date: str = datetime.now().isoformat()
    died_date: str = datetime.now().isoformat()
    def __init__(self,
                    xauthor:str,
                    xemail:str,
                    xbirth_date:str,
                    xdied_date:str):
           self.author = xauthor
           self.email = xemail
           self.birth_date = xbirth_date
           self.died_date = xdied_date
    def __prep__(self):
            return f"{self.author}:{self.email}:{self.birth_date}:{self.xdied_date}"

class Book(rx.Model, table=True):
    title: str
    registdry: str = datetime.now().isoformat()
    
    def __init__(self,
                    xtitle:str,
                    xregistry:str):
           self.title = xtitle  
           self.registry = xregistry
    def __prep__(self):
            return f"{self.title}:{self.registry}"

class Book_author(rx.Model, table=True):
    book_id: int= sqlmodel.Field(foreign_key="book.id")
    author_id: int= sqlmodel.Field(foreign_key="author.id")

class queryAuthor(rx.State):
    bookSta:list(Book)
    authorSta:list(Author)
    book_authorState:list(Book_author)

    def authorRead(self) -> list(Author):
        with rx.session as session:
           a = session.query(Author)
           authorlist = []
           for i in a:
               authorlist.append(i)
        return authorlist
    
    def bookRead(self) -> list(Book):
        with rx.session as session:
           a = session.query(Book)
           booklist = []
           for i in a:
               booklist.append(i)
        return booklist

    def book_authorRead(self) -> list(Book_author):
        with rx.session as session:
           a = session.query(Book_author)
           book_authorlist = []
           for i in a:
               book_authorlist.append(i)
        return book_authorlist
    def add_book(self, title: str, registry: str):
        new_book = Book(title=title, registry=registry)
        with rx.session as session:
            session.add(new_book)
            session.commit()
            session.refresh(new_book)
        return new_book

    def add_author(self, author: str, email: str, birth_date: str, died_date: str):
        new_author = Author(author=author, email=email, birth_date=birth_date, died_date=died_date)
        with rx.session as session:
            session.add(new_author)
            session.commit()
            session.refresh(new_author)
        return new_author
    def add_book_author(self, book: Book, author: Author):
        new_book_author = Book_author(book_id=book.id, author_id=author.id)
        with rx.session as session:
            session.add(new_book_author)
            session.commit()
            session.refresh(new_book_author)
        return new_book_author

    def remove_book(self, id: int):
        with rx.session as session:
            session.query(Book).filter(Book.id == id).delete()
            session.commit()

    def remove_author(self, id: int):
        with rx.session as session:
            session.query(Author).filter(Author.id == id).delete()
            session.commit()
    
        