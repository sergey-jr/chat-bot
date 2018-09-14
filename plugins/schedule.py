import calendar
import json
import os

import pytz
from datetime import datetime

from kutana import Plugin

plugin = Plugin(name="Расписание")

submenu = {
    "one_time": False,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Расписание на сегодня"
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Расписание на завтра"
                },
                "color": "default"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"3\"}",
                    "label": "Расписание на понедельник"
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"4\"}",
                    "label": "Расписание на вторник"
                },
                "color": "default"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"5\"}",
                    "label": "Расписание на среду"
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"6\"}",
                    "label": "Расписание на четверг"
                },
                "color": "default"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"7\"}",
                    "label": "Расписание на пятницу"
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"8\"}",
                    "label": "Расписание на субботу"
                },
                "color": "default"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"9\"}",
                    "label": "Назад"
                },
                "color": "primary"
            }
        ]
    ]
}


@plugin.on_text("Расписание")
async def schedule_submenu(message, attachments, env):
    await env.reply('Расписание (меню)', keyboard=json.dumps(submenu, ensure_ascii=False))


def readfile(day, group='у-156'):
    now = datetime.now(tz=pytz.timezone('Europe/Moscow'))
    now.replace(hour=0, minute=0, second=0, microsecond=0)
    if now.month > 8:
        year, next_year = now.year, now.year + 1
    if now.month < 7:
        year, next_year = now.year - 1, now.year
    w = 0
    for m in range(9, 13):
        c = calendar.monthcalendar(year, m)
        flag = 0
        for x in c:
            if m > 9 and 0 not in x and c[0] == x:
                w += 1
            if m == 9:
                w += 1
            if x != c[0] and m > 9:
                w += 1
            if now.day in x and m == now.month:
                flag = 1
                break
        if flag:
            break
    if now.year == next_year:
        for m in range(1, 7):
            c = calendar.monthcalendar(next_year, m)
            flag = 0
            for x in c:
                if 0 not in x and x == c[0]:
                    w += 1
                if x != c[0]:
                    w += 1
                if now.day in x and m == now.month:
                    flag = 1
                    break
            if flag:
                break
    week = w
    week_day = day
    try:
        cwd = "{}/{}".format(os.getcwd(), group)
        with open(os.path.join(cwd, "schedule.json"), mode='r', encoding='utf-8') as file:
            s = file.read()
            s = s.replace('\n', '')
            s = json.loads(s)[str(week_day)]
            t = ''
            for x in s:
                if isinstance(s[x], dict) and s[x]['subject']:
                    t += s[x]['time'] + ' ' + s[x]['subject'] + ' ' + s[x]['room'] + '\n'
                elif isinstance(s[x], list) or isinstance(s[x], tuple):
                    if week % 2 and s[x][0]:
                        t += s[x][0]['time'] + ' ' + s[x][0]['subject'] + ' ' + s[x][0]['room'] + '\n'
                    if s[x][1] and not week % 2:
                        t += s[x][1]['time'] + ' ' + s[x][1]['subject'] + ' ' + s[x][1]['room'] + '\n'
            if not week % 2:
                week = 'знаменатель'
            else:
                week = 'числитель'
            message = (week, t) if s else "Похоже у тебя выходной"
    except Exception as err:
        message = 'error! %s: %s' % (type(err), err)
    return message


@plugin.on_startswith_text("расписание на", "schedule for")
async def schedule(message, attachments, env):
    # TODO настройки языка, группы
    now = datetime.now(tz=pytz.timezone('Europe/Moscow'))
    week_day = now.weekday() + 1
    week_days = {"ru": ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье"],
                 "en": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}
    days = {"en": {"today": week_day, "tomorrow": week_day + 1},
            "ru": {"сегодня": week_day, "завтра": week_day + 1}}
    for i in range(1, 8):
        days["ru"][week_days["ru"][i - 1]] = i
        days["en"][week_days["en"][i - 1]] = i
    text = "{}:\n{}".format(message.text, readfile(days["ru"][env.body]))
    await env.reply(text)
