from db import get_db, use_db
from werkzeug.security import generate_password_hash, check_password_hash



@use_db
def create_user(db, username, password):
    password_hash = generate_password_hash(password)

    cursor = db.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    db.commit()

    return cursor.lastrowid

@use_db
def login_user(db, username, password):
    user = db.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()

    if user is None:
        return None

    id = user["id"]
    if check_password_hash(user["password_hash"], password):
        return id
