from db import use_db
from repositories.utils import get_id


@use_db
def get_albums(db):
    res = db.execute(
        "SELECT * FROM Albums"
    ).fetchall()

    return res



@get_id
@use_db
def update_album(db, user_id, album_id, name, description, year):
    if user_id is not None:
        db.execute(
            """
            UPDATE Albums
            SET name        = ?,
                description = ?,
                year        = ?
            WHERE id = ?
            """,
            (name, description, year, album_id)
        )
        db.commit()

@get_id
@use_db
def delete_album(db, user_id, album_id):
    if user_id is not None:
        res = db.execute(
            "DELETE FROM Albums WHERE id = ?",
            (album_id,)
        )
        db.commit()


@use_db
def get_album(db, album_id):
    res = db.execute(
        "SELECT * FROM Albums WHERE id = ?",
        (album_id,)
    ).fetchone()

    return res

@get_id
@use_db
def add_album(db, user_id, name, description, year):
    if user_id is not None:
        db.execute(
            "INSERT INTO Albums (name, description, year) VALUES (?, ?, ?)",
            (name, description, year)
        )
        db.commit()
