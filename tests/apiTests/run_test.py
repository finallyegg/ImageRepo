from util import register, authenticate, get_json_synchronous, post_json_synchronous, put_json_synchronous, delete_json_synchronous, post_file_synchronous
import filecmp

user1 = {"username": "usr1", "password": "123456", "email": "1@gmail.com"}
user2 = {"username": "usr2", "password": "123456", "email": "2@gmail.com"}
img1 = "tests/testImages/1.jpg"
img1Meta = {"description": "des", "isPrivate": 0, "accessKey": "0000"}

notValidImg = "tests/testImages/notValid.txt"


def singleUserTest():

    print("---------Now TESTING SINGLE USER---------")
    post_json_synchronous("/reset", "", "")
    register(user1["username"], user1["email"], user1["password"])
    token = authenticate(user1["email"], user1["password"])
    assert len(token) != 0
    # test image upload
    response = post_file_synchronous("/images", token, img1, img1Meta)
    assert response.status_code == 200
    img_id = response.json()["id"]
    print("Passed!")

    print("---------Now TESTING Public Access---------")
    # test get Img and whehter they are same
    img_url = "/images/" + str(img_id)
    getResponse = get_json_synchronous(img_url, token)
    assert getResponse.status_code == 200
    assert filecmp.cmp(img1, "outputs/1.jpg")
    print("Passed!")

    print("---------Now TESTING Invalid Upload---------")
    # test invalid image
    response = post_file_synchronous("/images", token, notValidImg, img1Meta)
    assert response.status_code == 400

    img_url = "/images/" + str(img_id)
    deleteResponse = delete_json_synchronous(img_url, token)
    assert deleteResponse.status_code == 202
    print("Passed!")


def multiUserTest():

    print("---------Now TESTING TWO USER With One Pic---------")
    post_json_synchronous("/reset", "", "")
    register(user1["username"], user1["email"], user1["password"])
    register(user2["username"], user2["email"], user2["password"])

    usr1_token = authenticate(user1["email"], user1["password"])
    usr2_token = authenticate(user2["email"], user2["password"])

    # test image upload
    response = post_file_synchronous("/images", usr1_token, img1, img1Meta)
    assert response.status_code == 200
    img1_id = response.json()["id"]
    img1_url = "/images/" + str(img1_id)
    getResponse = get_json_synchronous(img1_url, usr2_token)
    assert getResponse.status_code == 200
    assert filecmp.cmp(img1, "outputs/1.jpg")
    print("Passed!")

    print("---------Now Testing private Access---------")
    putResponse = put_json_synchronous(
        img1_url, {"description": "des", "isPrivate": 1, "accessKey": "0123"}, usr1_token)
    assert putResponse.status_code == 200
    assert putResponse.json()["locked"] == True
    getResponse = get_json_synchronous(img1_url, usr2_token)
    assert getResponse.status_code == 401

    putResponse = put_json_synchronous(
        img1_url, {"description": "des", "isPrivate": 0, "accessKey": "0123"}, usr1_token)
    getResponse = get_json_synchronous(img1_url, usr2_token)
    assert getResponse.status_code == 200
    print("Passed!")

    print("---------TESTING USER UPLOAD SAME IMAGE---------")
    img2_resp = post_file_synchronous("/images", usr2_token, img1, img1Meta)
    img2_id = img2_resp.json()["id"]

    deleteResponse = delete_json_synchronous(img1_url, usr1_token)
    assert deleteResponse.status_code == 202
    getResponse = get_json_synchronous(img1_url, usr2_token)
    assert getResponse.status_code == 200
    print("Passed!")

    print("---------TESTING SAFE DELETION---------")
    img2_url = "/images/" + str(img2_id)
    deleteResponse = delete_json_synchronous(img2_url, usr2_token)
    assert deleteResponse.status_code == 202
    print("Passed!")


def permissionTest():
    post_json_synchronous("/reset", "", "")

    print("---------Testing Unauth Post---------")
    response = post_file_synchronous("/images", "", img1, img1Meta)
    assert response.status_code != 200
    print("Passed!")

    register(user1["username"], user1["email"], user1["password"])
    register(user2["username"], user2["email"], user2["password"])

    usr1_token = authenticate(user1["email"], user1["password"])
    usr2_token = authenticate(user2["email"], user2["password"])

    print("---------Testing Access control---------")
    response = post_file_synchronous("/images", usr1_token, img1, img1Meta)
    img1_url = "/images/" + str(response.json()["id"])
    putResponse = put_json_synchronous(
        img1_url, {"description": "des", "isPrivate": 0, "accessKey": "0123"}, usr2_token)
    deleteResponse = delete_json_synchronous(img1_url, usr2_token)
    assert putResponse.status_code == 401
    assert deleteResponse.status_code == 401
    print("Passed!")


singleUserTest()
multiUserTest()
permissionTest()
