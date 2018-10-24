import copy
import json
import os
import re

from kutana import Plugin
import keyboards, settings
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


def parse_pair(pair):
    subject, room = pair, ''
    if ',' in pair and '/' in pair:
        res = pair.split('/')
        has_not_pair = ['None', 'пары нет']
        if any([i in pair for i in has_not_pair]):
            if res[0] in has_not_pair:
                res[1] = res[1].split(',')
                subject = '/'.join([res[0], res[1][0]])
                room = '/'.join([res[0], res[1][1]])
            if res[1] in has_not_pair:
                res[0] = res[0].split(',')
                subject = '/'.join([res[0][0], res[1]])
                room = '/'.join([res[0][1], res[1]])
        else:
            res = [item.split(',') for item in res]
            subject = '/'.join([res[0][0], res[1][0]])
            room = '/'.join([res[0][1], res[1][1]])
    elif ',' in pair:
        subject, room = pair.split(',')
    return {"subject": subject, "room": room}


def parse_row(high, low, day):
    time = high[0]
    res = None
    if low[day] and high[day] and high[day] != low[day]:
        res = [{'time': time}, {'time': time}]
        res[0].update(parse_pair(high[day]))
        res[1].update(parse_pair(low[day]))
    elif low[day] and not high[day]:
        res = [{}, {'time': time}]
        res[1].update(parse_pair(low[day]))
    elif high[day]:
        res = {'time': time}
        res.update(parse_pair(high[day]))
    return res


def parse_csv(url):
    file_data = urllib.request.urlopen(url)
    data_to_write = file_data.read().decode('windows-1251')
    data_to_write = re.sub('\r', '', data_to_write)
    data_to_write = data_to_write.split('\n')
    data_to_write = [i.split(';') for i in data_to_write]
    n = (len(data_to_write) - 1) // 2
    res = {}
    for i in range(len(data_to_write[0]) - 1):
        res[str(i + 1)] = {}

    for i in range(n):
        high = data_to_write[i * 2 + 1]
        low = data_to_write[(i + 1) * 2]
        if any(high[1:]) or any(low[1:]):
            for k in range(1, len(high)):
                row = parse_row(high, low, k)
                if row is not None:
                    res[str(k)][str(i + 1)] = row
    res_1 = copy.deepcopy(res)
    for k in res:
        if not res[k] or not all(res[k]):
            res_1.pop(k)
    res = res_1
    return json.dumps(res, ensure_ascii=False)


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
                    res = parse_csv(url)
                    file.write(res)
                text = 'Ok'
                file.close()
            except Exception as err:
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
            if group:
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
                        res = parse_csv(url)
                        file.write(res)
                    text = 'Ok'
                    file.close()
                except Exception as err:
                    await env.request('messages.send', user_id=100458394, message='error! %s: %s' % (type(err), err))
            else:
                text = 'Вы можете загрузить расписание для группы: ' + group
        else:
            text = 'Разрешенные форматы:' + ' '.join(types)
    else:
        text = 'Доступ запрещен'
    await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main_admin, ensure_ascii=False))
