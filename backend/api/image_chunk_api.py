from backend.models.blob_schema import Blob
from backend.models.user_schema import User
from backend.db import session_scope
from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request
import json
import hashlib
import base64
from werkzeug.utils import secure_filename
from backend.models.image_schema import ImageChunk, ImageChunkDTO
from backend.models.blob_schema import Blob
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
from backend.models.lru_cache import LRUCache
import os

image_chunk_api = Blueprint("image_chunk_api", __name__)
lru_size = 50
lru_cache = LRUCache(lru_size)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


@image_chunk_api.route("/images/<int:image_id>", methods=["DELETE"])
@jwt_required
def deleteImage(image_id):
    try:
        current = get_jwt_identity()
        with session_scope() as session:

            image_chunk = session.query(ImageChunk).get(image_id)
            if current != image_chunk.creator_id:
                return {}, 401

            lru_cache.remove(image_id)
            image_DTO = ImageChunkDTO.from_schema_object(image_chunk)
            image_name = image_DTO.name
            hash_list = json.loads(image_DTO.pieceJSON)

            for h in hash_list:
                blob = session.query(Blob).get(h)
                blob.count -= 1

                if blob.count == 0:
                    blob.delete()
                    os.remove(app.config["BLOB_URI"] + h)
            session.commit()
            session.flush()

            return jsonify({}), 200

    except Exception as ex:
        print(ex)
        return {}, 400


@image_chunk_api.route("/images/<int:image_id>", methods=["PUT"])
@jwt_required
def uploadImageMeta(image_id):
    try:
        current = get_jwt_identity()
        description, isPrivate, accessKey = request.json[
            "description"], bool(request.json["isPrivate"]), request.json["accessKey"]
        with session_scope() as session:

            image_chunk = session.query(ImageChunk).get(image_id)

            if current != image_chunk.creator_id:
                return {}, 401

            if isPrivate == None or accessKey == None:
                raise ValueError("Invalid Param")

            image_chunk.locked = isPrivate
            image_chunk.accessKey = accessKey
            session.commit()
            session.flush()

            retval = ImageChunkDTO.from_schema_object(image_chunk).serialize(
                isCreator=(current == image_chunk.creator_id))
            return jsonify(retval), 200

    except Exception as ex:
        print(ex)
        return {}, 400


@image_chunk_api.route("/images", methods=["POST"])
@jwt_required
def uploadImage():
    try:
        current = get_jwt_identity()
        file, description, isPrivate, accessKey = request.files["file"], request.form[
            "description"], bool(request.form["isPrivate"]), request.form["accessKey"]
        with session_scope() as session:
            if not file or not allowed_file(file.filename) or isPrivate == None or (isPrivate == True and not accessKey):
                raise ValueError("Empty file or Param")

            filename = secure_filename(file.filename)
            payload = file.read()

            if len(payload) == 0:
                raise ValueError("Empty file")

            hashes_json = json.dumps(encodeAndStore(payload))

            image_chunk = ImageChunk(
                name=filename, creator_id=current, pieceJSON=hashes_json, locked=isPrivate, accessKey=accessKey)
            session.add(image_chunk)
            session.flush()

            retval = ImageChunkDTO.from_schema_object(image_chunk).serialize(
                isCreator=(current == image_chunk.creator_id))
            return jsonify(retval), 200

    except Exception as ex:
        print(ex)
        return {}, 400


@image_chunk_api.route("/images/<int:image_id>", methods=["GET"])
@jwt_required
def getImage(image_id):
    try:
        current = get_jwt_identity()
        accessKey = request.args['accesskey'] if request.args else None
        with session_scope() as session:

            image_chunk = session.query(ImageChunk).get(image_id)
            temp_image = None
            image_DTO = ImageChunkDTO.from_schema_object(image_chunk)
            image_name = image_DTO.name
            hash_list = json.loads(image_DTO.pieceJSON)

            if image_DTO.locked and current != image_DTO.creator and accessKey != image_DTO.accessKey:
                return {"msg": "no permission"}, 401

            temp_image = bytearray()
            cache = lru_cache.get(image_id)
            if cache != -1:
                temp_image = cache
            else:
                for blob_name in hash_list:
                    f = open(app.config['BLOB_URI'] + blob_name, "rb")
                    temp_image += f.read()
                    f.close()

                f = open(app.config['OUTPUT_URI'] + image_name, "wb")
                f.write(temp_image)
                f.close()

                if not image_DTO.locked:
                    lru_cache.put(image_id, temp_image)

            encoded_string = base64.b64encode(temp_image).decode()
            retval = ImageChunkDTO.from_schema_object(image_chunk).serialize(
                isCreator=(current == image_DTO.creator))
            # retval.update({"image_date": encoded_string})

            return jsonify(retval), 200

    except Exception as ex:
        print(ex)
        return {}, 400


def encodeAndStore(payload):
    with session_scope() as session:
        hashes = []

        i = 0
        while i < len(payload):
            blob = None
            if i + 4096 >= len(payload):
                blob = payload[i: len(payload)]
            else:
                blob = payload[i: i+4096]
            sha256Hash = hashlib.sha256()
            sha256Hash.update(blob)
            b32_code = base64.b32encode(
                sha256Hash.digest()).decode("ascii")

            blob_chunk = session.query(Blob).get(b32_code)
            if blob_chunk != None:
                blob_chunk.count += 1
                session.commit()
            else:
                blob_chunk = Blob(id=b32_code, count=1)
                f = open(app.config["BLOB_URI"] + b32_code, "wb")
                f.write(blob)
                f.close()
                session.add(blob_chunk)

            session.flush()
            hashes.append(b32_code)
            i += 4096
        return hashes


@image_chunk_api.route("/reset", methods=["POST"])
def resetImage(image_id):
    try:
        with session_scope() as session:
            lru_cache = LRUCache(lru_size)

            session.query(ImageChunk).delete()
            session.query(User).delete()
            session.query(Blob).delete()

            import shutil
            shutil.rmtree(app.config["BLOB_URI"])
            shutil.rmtree(app.config["OUTPUT_URI"])

            return jsonify(retval), 200

    except Exception as ex:
        print(ex)
        return {}, 400
