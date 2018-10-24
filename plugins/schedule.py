import calendar
import json
import os

import pytz
from datetime import datetime, timedelta

from kutana import Plugin

import settings
import keyboards

plugin = Plugin(name="Расписание")


@plugin.on_text("Расписание")
async def schedule_submenu(message, attachments, env):
    user_setting = settings.load_settings(message.from_id)
    if user_setting:
        await env.reply('Расписание (меню)', keyboard=json.dumps(keyboards.schedule_menu, ensure_ascii=False))
    else:
        text = 'Для начала установите группу через пункт меню настройки.'
        await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main, ensure_ascii=False))


def get_subgroups_text(time, subject, room):
    if "/" not in subject:
        return " ".join([time, subject, room]) + '\n'
    else:
        subject = subject.split("/")
        room = room.split("/")
        return "{} {}({})/{}({})\n".format(time, subject[0], room[0], subject[1], room[1])


def read_file(**kwargs):
    try:
        group = kwargs.get('group', None)
        week = kwargs.get('week', None)
        delta = kwargs.get('delta', None)
        week_day = kwargs.get('weekday', None)
        date = kwargs.get('date', None)
        timezone = pytz.timezone('Europe/Moscow')
        now = datetime.now(tz=timezone) + timedelta(days=delta) if date is None else date
        cwd = "{}/{}".format(os.getcwd(), group)
        with open(os.path.join(cwd, "schedule.json"), mode='r', encoding='utf-8') as file:
            s = file.read()
            s = s.replace('\n', '')
            s = json.loads(s)[str(week_day)]
            t = ''
            for x in s:
                if isinstance(s[x], dict) and s[x]:
                    if delta == 0:
                        start, end = s[x]['time'].split('-')
                        start = datetime.strptime(start, '%H.%M').replace(day=now.day, month=now.month, year=now.year)
                        end = datetime.strptime(end, '%H.%M').replace(day=now.day, month=now.month, year=now.year)
                        start, end = timezone.localize(start), timezone.localize(end)
                        if start <= now <= end or start > now:
                            t += get_subgroups_text(s[x]['time'], s[x]['subject'], s[x]['room'])
                    else:
                        t += get_subgroups_text(s[x]['time'], s[x]['subject'], s[x]['room'])
                elif isinstance(s[x], list) or isinstance(s[x], tuple):
                    if week % 2 and s[x][0]:
                        if delta == 0:
                            start, end = s[x][0]['time'].split('-')
                            start = datetime.strptime(start, '%H.%M').replace(day=now.day, month=now.month,
                                                                              year=now.year)
                            end = datetime.strptime(end, '%H.%M').replace(day=now.day, month=now.month, year=now.year)
                            start, end = timezone.localize(start), timezone.localize(end)
                            if start <= now <= end or start > now:
                                t += get_subgroups_text(s[x][0]['time'], s[x][0]['subject'], s[x][0]['room'])
                        else:
                            t += get_subgroups_text(s[x][0]['time'], s[x][0]['subject'], s[x][0]['room'])
                    if s[x][1] and not week % 2:
                        if delta == 0:
                            start, end = s[x][1]['time'].split('-')
                            start = datetime.strptime(start, '%H.%M').replace(day=now.day, month=now.month,
                                                                              year=now.year)
                            end = datetime.strptime(end, '%H.%M').replace(day=now.day, month=now.month, year=now.year)
                            start, end = timezone.localize(start), timezone.localize(end)
                            if start <= now <= end or start > now:
                                t += get_subgroups_text(s[x][0]['time'], s[x][1]['subject'], s[x][0]['room'])
                        else:
                            t += get_subgroups_text(s[x][1]['time'], s[x][1]['subject'], s[x][1]['room'])
            if not week % 2:
                week = 'знаменатель'
            else:
                week = 'числитель'
            if not t and delta == 0:
                t = 'Пары на сегодня закончились.'
            message = (week, t) if s else (week, "Похоже у тебя выходной")
    except KeyError:
        if not week % 2:
            week = 'знаменатель'
        else:
            week = 'числитель'
        message = (week, "Похоже у тебя выходной")
    except Exception as err:
        message = 'error! %s: %s' % (type(err), err), -1
    return message


def get_schedule(**kwargs):
    group = kwargs.get('group', 'у-156')
    w = kwargs.get('w', 0)
    delta = kwargs.get('delta', 1 if kwargs.get('day', None) else None)
    date = kwargs.get('date', None)
    timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz=timezone) + timedelta(days=delta) if not date else date
    now.replace(hour=0, minute=0, second=0, microsecond=0)
    day = kwargs.get('day', now.weekday() + 1)
    if w == 0:
        if now.month > 8:
            year, next_year = now.year, now.year + 1
        if now.month < 7:
            year, next_year = now.year - 1, now.year
        for m in range(9, 13):
            c = calendar.monthcalendar(year, m)
            flag = 0
            for x in c:
                if m > 9 and 0 not in x and c[0] == x:
                    w += 1
                if m == 9:
                    if 1 in x and settings.first09:
                        w += 1
                    elif 1 not in x:
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
    message = read_file(group=group, week=week, weekday=week_day, delta=delta, date=date)
    return message


@plugin.on_startswith_text("расписание на", "schedule for")
async def schedule(message, attachments, env):
    # TODO настройки языка
    user_setting = settings.load_settings(message.from_id)
    if user_setting:
        now = datetime.now(tz=pytz.timezone('Europe/Moscow'))
        week_day = now.weekday() + 1
        week_days = {"ru": ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье"],
                     "en": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}
        days = {"en": {"today": {"day": week_day, "delta": 0},
                       "tomorrow": {"day": week_day + 1 if week_day in range(6) else 1, "delta": 1}},
                "ru": {"сегодня": {"day": week_day, "delta": 0},
                       "завтра": {"day": week_day + 1 if week_day in range(6) else 1, "delta": 1}}}
        for i in range(1, 8):
            days["ru"][week_days["ru"][i - 1]] = i
            days["en"][week_days["en"][i - 1]] = i
        if env.body in days['ru'].keys():
            day = days["ru"][env.body]
        elif env.body in days['en'].keys():
            day = days["en"][env.body]
        else:
            day = datetime.strptime(env.body, '%d.%m.%Y').weekday() + 1
        tmp = ["today", "tomorrow", "сегодня", "завтра"]
        if env.body in tmp:
            res = get_schedule(delta=day["delta"], group=user_setting['group'])
            text = "{}({}/{}):\n{}".format(message.text, week_days['ru'][day["day"] - 1], res[0], res[1])
        elif (env.body in days['ru'].keys() or env.body in days['en'].keys()) and env.body not in tmp:
            res = get_schedule(day=day, group=user_setting['group'])
            text = "{}({}):\n{}".format(message.text, res[0], res[1])
            # next week
            res = get_schedule(day=day, w=1, group=user_setting['group'])
            text += "\n{}({}):\n{}".format(message.text, res[0], res[1])
        else:
            date = datetime.strptime(env.body, '%d.%m.%Y')
            res = get_schedule(date=date, group=user_setting['group'])
            text = "{}({}/{}):\n{}".format(message.text, week_days['ru'][day - 1], res[0], res[1])
    else:
        text = 'Для начала установите группу через пункт меню настройки.'
    await env.reply(text)
