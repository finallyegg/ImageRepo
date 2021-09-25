from backend.models.user_schema import User
from backend.db import session_scope
from argon2 import PasswordHasher
from flask import Blueprint
from flask import current_app as app
from flask import request
import json


register_user = Blueprint("register_user", __name__)


@register_user.route("/register", methods=["GET", "POST"])
def register():
    try:
        username, email = request.json['name'], request.json['email']
        with session_scope() as session:
            if (constraints_check(session, email)):
                ph = PasswordHasher()
                password = request.json['password']
                user = User(name=username, emailId=email, password=ph.hash(
                    password), isAdmin=False)
                session.add(user)
            else:
                raise ValueError("Already in Use")
            return {}, 201
    except Exception as ex:
        print(ex)
        return {}, 400


def constraints_check(session, emailId):
    no_user = session.query(User).filter(User.emailId == emailId).count()
    if no_user > 0:
        return False
    else:
        return True
