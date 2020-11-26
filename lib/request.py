import json


def request_user_roles(server_id: str, user_id: str):
    with open("Server/{}/User/{}.json".format(server_id, user_id), encoding='utf-8') as fp:
        data = json.load(fp)
    return data['roles']


def request_user_jail(server_id: str, user_id: str):
    with open("Server/{}/User/{}.json".format(server_id, user_id), encoding='utf-8') as fp:
        data = json.load(fp)
    return data['jail']


def request_jail_role(server_id: str):
    with open("Server/{}/knast.json".format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    return data['role']


def request_jail_log(server_id: str):
    with open("Server/{}/knast.json".format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    return data['log']
