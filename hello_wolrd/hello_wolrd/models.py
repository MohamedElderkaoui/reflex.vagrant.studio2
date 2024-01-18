import reflex as rx
from datetime import datetime

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
    bookSta: list(Book)
    authorSta: list(Author)
    book_authorState: list(Book_author)

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
        new_author = Author(
            author=author, email=email, birth_date=birth_date, died_date=died_date
        )
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


def book_form():
    return rx.Vstack(
        rx.Label("Title"),
        rx.form(
            rx.TextInput("title"),
            # registdry
            rx.TextInput("registry", placeholder="YYYY"),
            rx.Checkbox(value=["english"], label="English"),
            rx.Button(
                "Submit",
                on_click=lambda _: book().add_book(
                    rx.get("title"),
                    registdry=int(rx.get("registry")),
                    english=(bool)(rx.get("english"))[0],
                ),
            ),
        ),
    )


def book_form_edit(self, book_id):
    booka = book().get_book(book_id)
    return rx.Vstack(
        rx.Label("Title"),
        rx.form(
            rx.TextInput("title", value=booka.title),
            # registdry
            rx.TextInput("registry", value=booka.registry, placeholder="YYYY"),
        ),
    )


def book_form_delete(self, book_id):
    with rx.session as session:
        session.query(Book).filter(Book.id == book_id).delete()
        session.commit()

        @app.route("/books/<string:action>/<string:book_id>")
        async def books(action, book_id):
            if action == "edit":
                return book_form_edit(book_id)
            elif action == "delete":
                return rx.page(
                    rx.vstack(
                        rx.Heading("Are you sure you want to delete this book?"),
                        rx.Button(
                            "Yes",
                            on_click=lambda _: book().remove_book(book_id),
                        ),
                        rx.Button("No", on_click=lambda _: book().show_books()),
                    )
                )
            else:
                return book().show_books()


# import DBManager
import DBManager


def get_db():  # hello_wolrd\reflex.db
    db = DBManager.DBManager()

    @db.route("/books/<id>")
    class BookHandler(rx.View):
        def init(self):
            self.book = None
            self.error = ""
            self.load_data(id)

            def load_data(self, id):
                try:
                    self.book = db.get_book(id)
                except Exception as e:
                    pass
                # print(e)
                if not self.book:
                    self.error = f"No book with ID {id}"
                else:
                    self.error = ""

    return db


class book:
    @staticmethod
    def show_books(books: list[Book]):
        if not books:
            return rx.Label("No Books Found")
        else:
            return rx.Table(
                headers=["ID", "Title", "registdry"],
                rows=[
                    (b.id, b.title, str(b.registdry))
                    for b in sorted(
                        books, key=lambda x: (not x.is_english, -x.registdry)
                    )
                ],
            ).set_style(border="1px solid black")

    @staticmethod
    def add_book(title: str, registdry: str):
        db = get_db()
        with db.session.begin(subtransactions=True) as session:
            new_book = Book(title=title, registdry=registdry)
            session.add(new_book)
            session.commit()
            session.refresh(new_book)
        return new_book

    @staticmethod
    def remove_book(id: int):
        db = get_db()
        with db.session.begin(subtransactions=True) as session:
            session.query(Book).filter(Book.id == id).delete()
            session.commit()

    @staticmethod
    def get_book(id: int):
        db = get_db()
        with db.session.begin(subtransactions=True) as session:
            book = session.query(Book).filter(Book.id == id).first()
        return book


class authors:
    @staticmethod
    async def show_authors(authors: list[Author]) -> rx.component:
        if not authors:
            return rx.Label("No Authors Found")
        else:
            """
            Authorname
            email
            birth_date
            died_date"""
            return rx.Table(
                headers=["ID", "Authorname", "email", "birth_date", "died_date"],
                rows=[(a.author, a.email, a.birth_date, a.died_date) for a in authors],
            ).set_style(
                border="1px solid black",
                display="flex",
                flex_direction="column",
                height="100%",
                width="100%",
            )

    @staticmethod
    async def add_author(authorname: str, email: str, birth_date: str, died_date: str):
        db = get_db()
        with rx.session.begin(subtransactions=True) as session:
            new_author = Author(
                author=authorname,
                email=email,
                birth_date=birth_date,
                died_date=died_date,
            )
            session.add(new_author)
            session.commit()
            session.refresh(new_author)
        return new_author

    @staticmethod
    async def remove_author(id: int):
        db = get_db()
        with rx.session.begin(subtransactions=True) as session:
            session.query(Author).filter(Author.id == id).delete()
            session.commit()

    @staticmethod
    async def get_author(id: int):
        db = get_db()
        with rx.session.begin(subtransactions=True) as session:
            author = session.query(Author).filter(Author.id == id).first()
        return author

    @staticmethod
    async def update_author(
        id: int, authorname: str, email: str, birth_date: str, died_date: str
    ):
        db = get_db()
        with rx.session.begin(subtransactions=True) as session:
            author = session.query(Author).filter(Author.id == id).first()
            # is diferent
            if author.author != authorname:
                author.author = authorname
            if author.email != email:
                author.email = email
            if author.birth_date != birth_date:
                author.birth_date = birth_date
            if author.died_date != died_date:
                author.died_date = died_date
            session.commit()
            session.refresh(author)
        return author


from hello_wolrd import app
def  author_form():
    return rx.vstack(
        rx.Heading("Add Author"),
        rx.Heading("Authorname"),
        rx.TextInput(),
        rx.Heading("email"),    
        rx.TextInput(),
        rx.Heading("birth_date"),
        rx.TextInput(),
        rx.Heading("died_date"),
        rx.TextInput(),
        rx.Button("Submit", on_click=lambda _: authors().add_author(rx.get("title"), rx.get("email"), rx.get("birth_date"), rx.get("died_date"))),
    )
def author_form_update(self, id):
    with rx.session.begin(subtransactions=True) as session:
        db = session.query(Author).filter(Author.id == id).first()
        return rx.vstack(
            rx.Heading("Update Author"),
            rx.Heading("Authorname"),
            rx.TextInput().set_value(db.author.Authorname),
            rx.Heading("email"),
            rx.TextInput().set_value(db.author.email),
            rx.Heading("birth_date"),
            rx.TextInput().set_value(db.author.birth_date),
            rx.Heading("died_date"),
            rx.TextInput().set_value(db.author.died_date),
            rx.Button(
                "Submit",
                on_click=lambda _: authors().update_author(
                    rx.get("title"),
                    rx.get("email"),
                    rx.get("birth_date"),
                    rx.get("died_date")
                )
            )
        )
def book_form_update(self,id):
    with rx.session.begin(subtransactions=True) as session:
        db = session.query(
            Book
        ).filter(Book.id == id).first()
        return rx.vstack(
            rx.Heading("Update Book"),
            rx.Heading("Title"),
            rx.TextInput().
            set_value(db.book.
                      
                      title),
            rx.Heading("registry"),
            rx.TextInput().
            set_value(db.book.
                      registry),
                rx.Button("Submit", on_click=lambda _: book().update_book(rx.get("title"), rx.get("registry")))
        )
@app.route("/")
def index(request):
    with rx.session.begin(subtransactions=True) as session:
        return rx.page(
            rx.vstack(
                rx.vstack(
                rx.Heading("Hello World"),
                rx.Button("Show Books", on_click=lambda _: book().show_books()),
                rx.Button("Show Authors", on_click=lambda _: authors().show_authors()),
                rx.Button("Add Book", on_click=lambda _: book_form().show()),  
                #update book
                rx.Button("Update Book", on_click=lambda _: book_form_update().show()), 
                rx.Button("Add Author", on_click=lambda _: author_form().show()),
                rx.Button("Update Author", on_click=lambda _: author_form().show()),
                rx.
                Button("Remove Author", on_click=lambda _: author_form().show()),
                rx.
                Button("Remove Book", on_click=lambda _: book_form().show()),
            ),
                rx.
                Button("Remove Book", on_click=lambda _: book_form_delete().show()),
                
            ).
            set_style(border="1px solid black")
            .set_style(**styles.template_page_style)
            .set_style(height="100%")
        )
    
    
@app.route("/books/<string:action>/<string:book_id>")
async def books(action, book_id):
    if action == "edit":
        return book_form_edit(book_id)
    elif action == "delete":
        return rx.page(
            rx.vstack(
                rx.Heading("Are you sure you want to delete this book?"),
                rx.Button(
                    "Yes",
                    on_click=lambda _: book().remove_book(book_id),
                ),
                rx.Button("No", on_click=lambda _: book().show_books()),
            )
        )
    else:
        return book().show_books()
@app.route("/books/")
def page_bo(self):
    return rx.page(
        rx.
        Button("Add Book", on_click=lambda _: book_form().show()),
        rx.
        Button("Remove Book", on_click=lambda _: book_form().show()),
    )
#-------------------------------AUTHORS-------------------------------------

@app.route("/authors/<string:action>/<string:author_id>")
async def authors(action, author_id):
    if action == "edit":
        return rx.page(
            author_form_update(author_id),
        )
    elif action == "update":
        with rx.session.begin(subtransactions=True) as session:
            return rx.page(
                author_form_update(author_id),
                rx.Button("Update", on_click=lambda _: authors().update_author(rx.get("title"), rx.get("email"), rx.get("birth_date"), rx.get("died_date"))),
            )
    elif action == "delete":
        return rx.page(
            rx.vstack(
                rx.Heading("Are you sure you want to delete this author?"),
                rx.Button(
                    "Yes",
                    on_click=lambda _: authors().remove_author(author_id),
                ),
                rx.Button("No", on_click=lambda _: authors().show_authors()),
            )
        )
    else:
        return authors().show_authors()
def show_error(title, message=""):  
    return rx.page(
        rx.Heading(title),
        rx.Heading(message),
    )
    