from flask import make_response, jsonify

from services.jwt_service import create_jwt


def auth_response(user_id):
    token = create_jwt(user_id)
    resp = make_response(jsonify({"ok": True}))
    resp.set_cookie("_at", token, httponly=True, samesite="Lax")
    return resp