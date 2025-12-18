from flask import Flask, render_template, jsonify, request, make_response, g

from db import close_db
from repositories.albums_repository import get_albums
from repositories.users_repository import create_user, login_user
from services.jwt_service import create_jwt, decode_jwt
from utils.auth_responce import auth_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("mainPage.html")

@app.route("/albums")
def albums():
    albums = get_albums()

    return render_template("albumsPage.html", albums=albums)

@app.route("/albums/add")
def albums_add():
    return render_template("addAlbum.html")

@app.route("/history")
def history():
    return render_template("historyPage.html")

@app.route("/about")
def about():
    return render_template("aboutPage.html")

@app.route("/register", methods=["GET"])
def register_get():
    ...

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("loginPage.html")


@app.route("/register", methods=["POST"])
def register_post():
    user_id = create_user(username="denis", password="123")

    if not user_id:
        return jsonify({"error": "invalid credentials"}), 401

    return auth_response(user_id)

@app.route("/login", methods=["POST"])
def login_post():
    user_id = login_user(username="denis", password="123")

    if not user_id:
        return jsonify({"error": "invalid credentials"}), 401

    return auth_response(user_id)



@app.before_request
def before_request():
    token = request.cookies.get("_at")

    payload = decode_jwt(token)

    if payload:
        g.user = {
            "id": payload
        }



@app.teardown_appcontext
def teardown(exepction):
    close_db()

if __name__ == '__main__':
    app.run(debug=True)
