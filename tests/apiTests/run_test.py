from util import register, get_json_synchronous, post_json_synchronous, put_json_synchronous, delete_json_synchronous, post_file_synchronous


def singleUserTest():
    post_json_synchronous("/reset", "", "")


singleUserTest()
