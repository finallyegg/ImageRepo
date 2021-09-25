from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from flask import jsonify, request
from flask import current_app as app
from argon2 import PasswordHasher
from backend.models.user_schema import User
from backend.db import read_only_session_scope


auth_api = Blueprint("auth_api", __name__)
password_hasher = PasswordHasher()
login_cache = {}


@auth_api.route("/login", methods=["POST"])
def authenticate():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    with read_only_session_scope() as session:
        user = session.query(User).filter(User.emailId == username).first()
        if user and password_hasher.verify(user.password, password):
            # OVERWRITE if it is called again.
            login_cache[user.id] = user
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
            # access_token = ()
        else:
            return jsonify({"msg": "Bad username or password"}), 401
