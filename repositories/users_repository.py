from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
def use_db(func):
    def wrapper(*args, **kwargs):
        db = get_db()
        try:
            return func(db, *args, **kwargs)
        finally:
            db.close()
    return wrapper

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
