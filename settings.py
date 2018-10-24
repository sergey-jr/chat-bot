import json
import os

token = 'bf90dcf53ded8e2759b4b799970569c42eee11adad2d0b2f031596bd2e227f9d469df88f7f7e5922cda23'

admins = [100458394]

groups_admins = {
    "у-156": [100458394, 69449070],
    "у-153": [327780936],
}

first09 = False


def load_settings(user):
    try:
        if 'settings' not in os.listdir(os.getcwd()):
            os.mkdir("{}/{}".format(os.getcwd(), 'settings'))
        file_name = "{}/settings/{}.json".format(os.getcwd(), user)
        file = open(file_name, mode='r', encoding='UTF-8')
        return json.loads(file.read())
    except FileNotFoundError:
        return None
