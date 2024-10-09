
import sqlite3

from flask import redirect, render_template, session, flash
from functools import wraps


DATABASE = ""


def register_db_name(database):
    global DATABASE
    DATABASE = database
    return


def SQL(query, params=()):
    try:
        with sqlite3.connect(DATABASE) as connect:
            connect.row_factory = sqlite3.Row
            c = connect.cursor()
            c.execute(query, params)
            tasks = c.fetchall()
        return tasks
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return -1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return -1


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
