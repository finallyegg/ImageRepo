import requests


def authenticate_as_admin():
    return authenticate("admin", "admin")


def authenticate(username, password):
    server_port = 5666
    json = {"username": username, "password": password}
    response = requests.post("http://localhost:" +
                             server_port + "/login", json=json)
    return response.json()['access_token']


def register(username, email, password):
    server_port = 5666
    json = {"name": username, "password": password, "email": email}
    return requests.post("http://localhost:" + server_port + "/register", json=json)


def get_json_synchronous(uri, access_token):
    server_port = 5666
    headers = {"Authorization": "Bearer " + access_token}
    return requests.get("http://localhost:" + server_port + uri, headers=headers)


def post_json_synchronous(uri, json_payload, access_token):
    server_port = 5666
    headers = {"Authorization": "Bearer " + access_token}
    return requests.post("http://localhost:" + server_port + uri, headers=headers, json=json_payload)


def put_json_synchronous(uri, json_payload, access_token):
    server_port = 5666
    headers = {"Authorization": "Bearer " + access_token}
    return requests.put("http://localhost:" + server_port + uri, headers=headers, json=json_payload)


def delete_json_synchronous(uri, access_token):
    server_port = 5666
    headers = {"Authorization": "Bearer " + access_token}
    return requests.delete("http://localhost:" + server_port + uri, headers=headers)


def post_file_synchronous(uri, access_token, file_path, file_meta):
    server_port = 5666
    headers = {"Authorization": "Bearer " + access_token}
    files = {'file': open(file_path, 'rb')}
    requests.post("http://localhost:" + server_port + uri,
                  headers=headers, files=files, data=file_meta)
