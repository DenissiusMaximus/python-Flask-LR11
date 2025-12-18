from flask import make_response, jsonify, url_for, redirect

from services.jwt_service import create_jwt


def auth_response(user_id):
    token = create_jwt(user_id)
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie("_at", token, httponly=True, samesite="Lax")

    return resp