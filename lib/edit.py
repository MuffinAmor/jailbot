import json


def edit_user_roles(server_id: str, user_id: str, input_data):
    with open("Server/{}/User/{}.json".format(server_id, user_id), encoding='utf-8') as fp:
        data = json.load(fp)
    data['roles'] = input_data
    with open("Server/{}/User/{}.json".format(server_id, user_id), 'w+') as fp:
        json.dump(data, fp, indent=4)


def edit_user_jail(server_id: str, user_id: str, input_data):
    with open("Server/{}/User/{}.json".format(server_id, user_id), encoding='utf-8') as fp:
        data = json.load(fp)
    data['jail'] = input_data
    with open("Server/{}/User/{}.json".format(server_id, user_id), 'w+') as fp:
        json.dump(data, fp, indent=4)


def edit_jail_role(server_id: str, input_data):
    with open("Server/{}/knast.json".format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    data['role'] = input_data
    with open("Server/{}/knast.json".format(server_id), 'w+') as fp:
        json.dump(data, fp, indent=4)


def edit_jail_log(server_id: str, input_data):
    with open("Server/{}/knast.json".format(server_id), encoding='utf-8') as fp:
        data = json.load(fp)
    data['log'] = input_data
    with open("Server/{}/knast.json".format(server_id), 'w+') as fp:
        json.dump(data, fp, indent=4)
