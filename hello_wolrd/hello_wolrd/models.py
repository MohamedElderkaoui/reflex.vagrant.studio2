import reflex as rx
from datetime import datetime
from styles import styles
import sqlmodel
import sqlmodelç
import User


class BaseModel(rx.sqlmodel.SQLModel):
    class Config:
        with rx.session() as session:
            session.add(
                User(
                    username="test",
                    email="mderkaoui10@gmail.com",
                    password="a",
                )
            )
            session.commit()


class Author(rx.Model, table=True):
    Authorname: str
    email: str
    birth_date: str = datetime.now().isoformat()
    died_date: str = datetime.now().isoformat()

    def __init__(self, xauthor: str, xemail: str, xbirth_date: str, xdied_date: str):
        self.author = xauthor
        self.email = xemail
        self.birth_date = xbirth_date
        self.died_date = xdied_date

    def __prep__(self):
        return f"{self.author}:{self.email}:{self.birth_date}:{self.xdied_date}"


class Book(rx.Model, table=True):
    title: str
    registdry: str = datetime.now().isoformat()

    def __init__(self, xtitle: str, xregistry: str):
        self.title = xtitle
        self.registry = xregistry

    def __prep__(self):
        return f"{self.title}:{self.registry}"


class Book_author(rx.Model, table=True):
    book_id: int = sqlmodel.Field(foreign_key="book.id")
    author_id: int = sqlmodel.Field(foreign_key="author.id")


class query(rx.State):
    books: list[Book] = rx.field(default=[])
    authors: list[Author]=rx.field(default=[])
    
    def get_books(self):
        with rx.session() as session:
            self.books=session.exec(
                Book.
                select()).scalars().all()
    def get_author(SELF):
        with rx.session as session:
            SELF            .authors=session.exec(
                Author.select()).scalars().all()
State=rx.State
class changeBookTitle(rx.
                      State):
    old_title:str
    new_title:str
    def on_apply(SELF, mgr):
        with rx.session as session:
            book_old=            session.exec(
                Book.select().where(                    Book.title==SELF.old_title)).scalar()          
            if not book_old:
                raise ValueError("No such book.")
            else:
                book_old.title=SELF.new_title
                mgr.next(SELF)

class addBook(rx.State):
    title: str
    registry:str
    def on_apply(SELF, mgr):
        with rx.session as session:
            bk=Book(title=SELF.title,registry=SELF.
                    registry)
            session.add(bk)
            session.commit()

            mgr.next(query())   
            
class addAuthor(rx.State):
    name : str
    email:str
    birth_date:str
    died_dated:str
    def on_apply(SELF, mgr):
        with rx.session  as session :
            author = Author(
                name   = SELF.name ,
                email = SELF.email ,
                birth_date = datetime.datetime.strptime(SELF.birth_date
                                                        ,"%Y-%m-%d") ,
                died_date = None if SELF.died_dated is None else datetime.
                datetime.strptime(SELF.died_dated, "%Y-%m-%d") 
            )
            
            session.add(author)
            session.commit()

class rmBook(rx.State):
    id : int
    def on_apply(SELF, mgr):
        with rx.session  as session :
              session.delete(
                  Book.
                  select().
                  where(Book.id==SELF.id)
              )
              session.commit()

class rmAuthor(
    rx.session
):
    id:int
    def on_apply(SELF, mgr):
        with rx.session  as session :
               session.delete(
                  Author.
                  select().
                  where(Author.id==SELF.id)
              )
               session.commit()
               
class changeBookregistry(rx.
                      State):
    old_registry:str
    new_registry:str
    def on_apply(SELF, mgr):
        with rx.session as session:
              book_old=            session.exec(
                  Book.
                  select().
                  where(             Book.registry==SELF.
                        old_registry)).scalar()
              if not book_old:
                  raise ValueError("No such book.")
              else:
                  book_old.registry = SELF.new_registry
                  mgr.next(display())
class changeAuthorEmal(rx.
                      State):
    old_email:str
    new_email:str
    def on_apply(SELF, mgr):
        with rx.session as session:
            author_old=          session.exec(
                Author.
                select().
                where((Author.email == SELF.old_email)
                ))
            if not author_old:
                raise ValueError("The email is not in the database or it does not belong to this book")
            else:
                for a in author_old:
                    a.email = SELF.new_email
                    mgr.go_back(2)
                    
class display(rx.Final):
    def action(self, mgr):
        with rx.session as session:
            books=session.query(Book).all()
            print("\n".join([str(book) for book in books]))
            