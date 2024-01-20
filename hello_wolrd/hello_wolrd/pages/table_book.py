"""The table_book page."""
from hello_wolrd.templates import template
from hello_wolrd.hello_wolrd.hello_wolrd import *
import reflex as rx

class State(rx.State):
    def __init__(self, books=None):
        self.books = books
@template("table_book")
def table_book() -> rx.Component:
    state = State()
    @state.depends
    def books():
        return query.get_books(state.books)
class BookRow(rx.Component):
    def render(self):
        return rx.table(
            rx.table_row(
                rx.table_cell(self.book.title),
                rx.table_cell(self.book.registry),
                
            )
        )

BookRow.bind(BookRow.book <-- rx.this.book)
BookRow.connect(BookRow.render > rx.parent.add_child)
TableBody = rx.Component.create(lambda : rx.table(rx.tbody
    .connect(BookRow.render > rx.parent.add_child)
    .bind(State.books).
    for_each(BookRow).
    add_child(AddButton)
    .add_child(rx.table_row(rx.table_cell()))
    .add_child(rx.table_row(rx.table_cell()))
))
class AddButton(rx.Component):
    def render(self):
        return rx.table_row(
            rx.table_cell(
                rx.link("Add Book", href="/add_book")
            )
        )
AddButton.connect(AddButton.render >> TableBody().add_child)

