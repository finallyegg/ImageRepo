from flask import Flask, send_from_directory
from flask_cors import CORS
from config import DevelopmentConfig
from flask_jwt_extended import JWTManager
from backend.api.auth_api import auth_api
from backend.api.register_user import register_user
from backend.api.image_chunk_api import image_chunk_api

import os

app = Flask(__name__, static_folder="../frontend/build")
CORS(app)
JWTManager(app)

app.config.from_object(DevelopmentConfig)

app.register_blueprint(auth_api)
app.register_blueprint(register_user)
app.register_blueprint(image_chunk_api)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return None, 404
    # if path != "" and os.path.exists(app.static_folder + "/" + path):
    #     return send_from_directory(app.static_folder, path)
    # else:
    #     return send_from_directory(app.static_folder, "index.html")
