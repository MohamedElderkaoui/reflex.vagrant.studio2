"""Welcome to Reflex!."""

from hello_wolrd import styles

# Import all the pages.zz
from hello_wolrd.pages import *

import reflex as rx

class State(rx.State):
    """Define empty state to allow access to rx.State.router."""


# Create the app.
app = rx.App(style=styles.base_style)
# export app to model.py

# 