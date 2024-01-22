"""The table_book page."""
import datetime
import typing
from hello_wolrd.templates import template
from hello_wolrd.hello_wolrd.hello_wolrd import query, AuthorForm, Author
import reflex as rx

class State(rx.State):
    def __init__(self, books=None):
        self.books = books or []
@template("table_book")
def table_book() -> rx.Component:
    state = State()
    @state.depends
    def books():
        return query.get_books(state.books)


class authorRow(rx.Component):
    def render(self):
        return rx.table(
            rx.table_row(
                rx.table_cell(self.book.title),
                rx.table_cell(self.book.registry),
                
            )
        )

authorRow.bind(authorRow.book <-- rx.this.book)
authorRow.connect(authorRow.render > rx.parent.add_child)
TableBody = rx.Component.create(lambda : rx.table(rx.tbody
    .connect(authorRow.render > rx.parent.add_child)
    .bind(State.books).
    for_each(authorRow).
    add_child(AddButton)
    .add_child(rx.table_row(rx.table_cell()))
    .add_child(rx.table_row(rx.table_cell()))
))
class AddButton(rx.Component):
    def render(self):
        return rx.table_row(
            rx.table_cell(
                rx.link("Add Author", href="/add_author")
            )
        )
AddButton.connect(AddButton.render >> TableBody().add_child)

BooksPage = rx.Component.create(lambda : rx.div(
    TableBody()
))
BooksPage.include_stylesheets("style.css")
BooksPage.connect(BooksPage.render > rx.window.document.body

)       
@rx.route(
    "/add_author",
    methods=["GET"])
def add_author():
    return rx.redirect("/add_author")
AuthorForm = rx.form(
    rx.vstack(
        rx.label("Name"),
        rx.input(
            name="name",
            type="text",
            
        ),
        rx.label("Email"),
        rx.input(
            name="email",
            type="text",
        ),
        rx.label("Birth Date"),
        rx.input(
            name="birth_date",
            type="date",
        ),
        rx.label("        died Date"),
        rx.input(
            name="died_date",
            type="date",
        ),
# save
        rx.button(
            "Save",
            type="submit",
            on_apply=rx.hold(rx.event, rx.event.data),
            
        ).
        bind(AuthorForm.data >> rx.hold(rx.event, rx.event.data))
    )
)

@rx.route(
    # update
    "/update_author",
    methods=["GET"])
class UpdateAuthorform(rx.Form):
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
            return [author]


def authors_bp() -> rx.Component:
    @rx.route("/authors")
    class AuthorsView (rx.View):
        async def on_get(_self) -> typing.Awaitable[typing.Any
                                                    ]:
            with rx.db.engine.begin() as conn :
                authors = await Author.select().gino.load(
                    "id", "name" , "email" , "birth_date" ,
                    "death_date").all()
                return {"authors": authors}
            return rx.page(
                "authors/index.html" ,
                title="Authors" ,
                data={"authors": authors})
            add_author_view = AddAuthorform.as_view()
            return rx.redirect(add_author_view)
            
rx.App.use("/authors" , authors_bp)