import json
import os

token = os.environ['TOKEN']

admins = [100458394]

groups_admins = {
    "у-156": [100458394],
    "у-153": [327780936],
}


def load_settings(user):
    try:
        file_name = "{}/settings/{}.json".format(os.getcwd(), user)
        file = open(file_name, mode='r', encoding='UTF-8')
        return json.loads(file.read())
    except FileNotFoundError:
        return None
