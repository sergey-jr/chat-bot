import json
import os

token = 'bf90dcf53ded8e2759b4b799970569c42eee11adad2d0b2f031596bd2e227f9d469df88f7f7e5922cda23'

admins = [100458394]

groups_admins = {
}

first09 = False


def load_settings(user):
    file_name = "{}\settings\\{}.json".format(os.getcwd(), user)
    with open(file_name, mode='r', encoding='UTF-8') as file:
        return json.loads(file.read())
