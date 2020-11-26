import json
import os


def create_server(server_id: str):
    if not os.path.isfile("Server"):
        try:
            os.mkdir("Server")
        except FileExistsError:
            pass
    if not os.path.isfile("Server/{}".format(server_id)):
        try:
            os.mkdir("Server/{}".format(server_id))
        except FileExistsError:
            pass
    if not os.path.isfile("Server/{}/User".format(server_id)):
        try:
            os.mkdir("Server/{}/User".format(server_id))
        except FileExistsError:
            pass
    if not os.path.isfile("Server/{}/knast.json".format(server_id)):
        data = {
            'role': None,
            'log': None,
        }
        with open("Server/{}/knast.json".format(server_id), 'w+') as fp:
            json.dump(data, fp, indent=4)


def delete_server(server_id: str):
    if os.path.isfile("Server/{}".format(server_id)):
        os.remove("Server/{}".format(server_id))


def create_user(server_id: str, user_id: str):
    if not os.path.isfile("Server/{}/User/{}.json".format(server_id, user_id)):
        data = {
            'roles': [],
            'jail': False
        }
        with open("Server/{}/User/{}.json".format(server_id, user_id), 'w+') as fp:
            json.dump(data, fp, indent=4)


