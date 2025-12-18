import sqlite3
import os
from flask import g

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "db.sqlite")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db():
    db = g.pop("db", None)
    if db is not None:
        db.close()

def use_db(func):
    def wrapper(*args, **kwargs):
        db = get_db()
        try:
            return func(db, *args, **kwargs)
        finally:
            db.close()
    return wrapper

