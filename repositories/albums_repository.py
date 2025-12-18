from db import use_db
from repositories.utils import get_id


@use_db
def get_albums(db):
    res = db.execute(
        "SELECT * FROM Albums"
    ).fetchall()

    return res

@use_db
@get_id
def add_album(db, user_id, name, description, year):
    if user_id is not None:
        res = db.execute(
            "INSERT INTO Albums VALUES (?, ?, ?, ?)",
            (user_id, name, description, year)
        )

        return res