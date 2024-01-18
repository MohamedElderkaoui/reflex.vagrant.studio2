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

class query(rx.State):
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
    
def book_form():
    return rx.Vstack(
        rx.Label('Title'),
        rx.form(
            rx.TextInput("title"),
            # registdry
            rx.TextInput(
                "registry",
                placeholder="YYYY"
                
            ),
            rx.Checkbox(
                value=["english"],
                label="English"
                ),
            rx.Button(
                'Submit',
                on_click=lambda _: book().add_book(rx.get('title'),
                                                    registdry=int(rx.get('registry')),
                                                    english=(bool)(rx.get('english'))[0])
                )
        )
    )
# import DBManager
import DBManager
def get_db():#hello_wolrd\reflex.db
    db = DBManager.DBManager()
    @db.route('/books/<id>')
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
                    self.error = f'No book with ID {id}'
                else:
                    
    
class book:
    @staticmethod
    def show_books(books: List[Book]):
        if not books:
            return rx.Label("No Books Found")
        else:
            return rx.Table(
                headers=['ID', 'Title', 'registdry'],
                rows=[(b.id, b.title, str(b.registdry)) for b
                      in sorted(books, key=lambda x: (not x.is_english
                                                      ,-x.registdry))]
                ).set_style(border='1px solid black')
    @staticmethod
    def add_book(title:str, registdry:str):
        db = get_db()
        with db.session.begin(subtransactions=True) as session:
            new_book = Book(title=title, registdry=registdry)
            session.add(new_book)
            
        
        
        
            
                
from hello_wolrd import app
@app.route('/books/<int:book_id>/authors/add')
async def add_author_to_book(request, book_id):
    return app.response.html(
        rx.Page(
            title='Add Author to Book',
            head=[],
            body=rx.HStack([
                rx.VStack([
                    rx.Link("/books", 'Back to Books'),
                    rx.Heading('Add an author to this book'),
                    ]),
                rx.Spacer(),
                book_form()
                ])
         ) )
@app.route('/books/<int:book_id>')