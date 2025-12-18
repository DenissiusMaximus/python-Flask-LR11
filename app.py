from flask import Flask, render_template, jsonify, request, make_response, g, url_for, redirect

from db import close_db
from repositories.albums_repository import get_albums, add_album, get_album, update_album, delete_album
from repositories.users_repository import create_user, login_user
from services.jwt_service import create_jwt, decode_jwt
from utils.auth_responce import auth_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("mainPage.html")

@app.route("/albums/<int:id>/delete", methods=["POST"])
def album_delete(id):
    delete_album(album_id=id)

    return redirect(url_for("albums"))

@app.route("/albums/<int:id>/edit", methods=["GET"])
def album_edit_get(id):
    album = get_album(id)

    if album is None:
        return jsonify({"error": "can not find this album"}), 401

    return render_template("editAlbum.html", album=album)


@app.route("/albums/<int:id>/edit", methods=["POST"])
def album_edit_post(id):
    name = request.form.get("name")
    description = request.form.get("description")
    year = request.form.get("year")

    update_album(name=name, description=description, year=year, album_id=id)

    return redirect(url_for("album_id", id=id))

@app.route("/albums", methods=["GET"])
def albums():
    albums = get_albums()

    return render_template("albumsPage.html", albums=albums)

@app.route("/albums/<int:id>")
def album_id(id):
    album = get_album(id)

    if album is None:
        return jsonify({"error": "can not find this album"}), 401

    return render_template("albumPage.html", album=album)

@app.route("/albums/add", methods=["GET"])
def albums_add_get():
    return render_template("addAlbum.html")

@app.route("/albums/add", methods=["POST"])
def albums_add_post():
    name = request.form.get("name")
    description = request.form.get("description")
    year = request.form.get("year")

    add_album(name=name, description=description, year=year)

    return redirect(url_for("albums"))

@app.route("/history")
def history():
    return render_template("historyPage.html")

@app.route("/about")
def about():
    return render_template("aboutPage.html")

@app.route("/register", methods=["GET"])
def register_get():
    return render_template("registerPage.html")

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("loginPage.html")


@app.route("/register", methods=["POST"])
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")
    password_confirm = request.form.get("password_confirm")

    if password != password_confirm:
        return render_template(
            "registerPage.html",
            error="Паролі не співпадають"
        )

    user_id = create_user(username=username, password=password)

    if not user_id:
        return render_template(
            "registerPage.html",
            error_messge="Користувач вже існує"
        )

    return auth_response(user_id)


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    # username = "denis", password = "123"
    user_id = login_user(username=username, password=password)

    if not user_id:
        return jsonify({"error": "invalid credentials"}), 401

    redirect(url_for("index"))

    return auth_response(user_id)

@app.route("/logout", methods=["POST"])
def logout_post():
    resp = make_response(redirect(url_for("index")))
    resp.delete_cookie("_at")

    return resp


@app.before_request
def before_request():
    token = request.cookies.get("_at")

    g.user = None

    payload = decode_jwt(token)

    if payload:
        g.user = {
            "id": payload
        }

@app.context_processor
def inject_user():
    if g.user:
        user_id = g.user["id"]["user_id"]
    else:
        user_id = None

    return {
        "current_user_id": user_id,
    }

@app.teardown_appcontext
def teardown(exepction):
    close_db()

if __name__ == '__main__':
    app.run(debug=True)
