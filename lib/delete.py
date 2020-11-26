import os


def delete_server(server_id: str):
    if os.path.isfile("Server/{}".format(server_id)):
        os.remove("Server/{}".format(server_id))


def delete_user(server_id: str, user_id: str):
    if os.path.isfile("Server/{}/User/{}.json".format(server_id, user_id)):
        os.remove("Server/{}/User/{}.json".format(server_id, user_id))
