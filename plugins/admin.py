import json
import os

from kutana import Plugin
from lib.csv_parser import CsvParser
import keyboards
import settings
import urllib.request

plugin = Plugin(name="Админка")


@plugin.on_text("Админка", "admin")
async def admin(message, attachments, env):
    if message.from_id in settings.admins:
        text = 'Вы можете загрузить расписание для любой группы'
    elif any([message.from_id in settings.groups_admins.values()]):
        group = ''
        for k in settings.groups_admins:
            if message.from_id in settings.groups_admins[k]:
                group = k
                break
        text = 'Вы можете загрузить расписание для группы: ' + group
    else:
        text = 'Доступ запрещен'
    await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main_admin, ensure_ascii=False))


@plugin.on_attachment("doc")
async def save_schedule(message, attachments, env):
    types = ['csv', 'txt', 'json']
    title, ext = attachments[0][5]['doc']['title'].split('.')
    url = attachments[0][5]['doc']['url']
    if message.from_id in settings.admins:
        if ext in types:
            try:
                if title not in os.listdir(os.getcwd()):
                    os.mkdir("{}/{}".format(os.getcwd(), title))
                file_name = 'schedule.json'
                file = open("{}/{}/{}".format(os.getcwd(), title, file_name), mode='w', encoding='UTF-8')
                if ext == 'json':
                    file_data = urllib.request.urlopen(url)
                    data_to_write = file_data.read().decode('utf-8')
                    file.write(data_to_write)
                elif ext == 'csv':
                    parser = CsvParser(url=url)
                    res = parser.parse()
                    file.write(res)
                text = 'Ok'
                file.close()
            except Exception as err:
                text = 'Произошла ошибка мы уже работаем над этим.'
                await env.request('messages.send', user_id=100458394, message='error! %s: %s' % (type(err), err))
        else:
            text = 'Разрешенные форматы:' + ' '.join(types)
    elif any([message.from_id in settings.groups_admins.values()]):
        if ext in types:
            group = ''
            for k in settings.groups_admins:
                if message.from_id in settings.groups_admins[k]:
                    group = k
                    break
            if group and group == title:
                try:
                    if title not in os.listdir(os.getcwd()):
                        os.mkdir("{}/{}".format(os.getcwd(), title))
                    file_name = 'schedule.json'
                    file = open("{}/{}/{}".format(os.getcwd(), title, file_name), mode='w', encoding='UTF-8')
                    if ext == 'json':
                        file_data = urllib.request.urlopen(url)
                        data_to_write = file_data.read().decode('utf-8')
                        file.write(data_to_write)
                    elif ext == 'csv':
                        parser = CsvParser(url=url)
                        res = parser.parse()
                        file.write(res)
                    text = 'Ok'
                    file.close()
                except Exception as err:
                    text = 'Произошла ошибка мы уже работаем над этим.'
                    await env.request('messages.send', user_id=100458394, message='error! %s: %s' % (type(err), err))
            else:
                text = 'Вы можете загрузить расписание для группы: ' + group
        else:
            text = 'Разрешенные форматы:' + ' '.join(types)
    else:
        text = 'Доступ запрещен'
    await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main_admin, ensure_ascii=False))
