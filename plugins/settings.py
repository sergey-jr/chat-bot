import json
import os
import re

import keyboards
from kutana import Plugin

import settings

plugin = Plugin(name="настройки")


@plugin.on_text('settings', 'настройки')
async def setting_menu(message, attachments, env):
    try:
        file_name = "{}/settings/{}.json".format(os.getcwd(), message.from_id)
        file = open(file_name, encoding="UTF-8", mode="r")
        text = file.read()
        file.close()
        text += "\nДля изменения настроек введите команду:\n" \
                "Обновить настройку <имя настройки>: <значение>\n" \
                "Доступные настройки: группа\n" \
                "Или\nОбновить настройки:\n и каждую настройку с новой строки с значением в  формате как указано выше"
    except FileNotFoundError:
        text = "Для создания настроек введите команду:\n" \
               "Сохранить настройки\n" \
               "группа*: <группа>\n" \
               "p.s. все вводить одним сообщением, недопуская ошибок, настройки в любом порядке\n" \
               "* - обязательный параметр"
    if message.from_id in settings.admins:
        await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main_admin, ensure_ascii=False))
    else:
        await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main, ensure_ascii=False))


@plugin.on_startswith_text('Сохранить настройки', 'Save settings')
async def settings_save(message, attachments, env):
    setting = {}
    s = [item.strip().split(": ") for item in env.body.split('\n')]
    for item in s:
        if item[0] in ['group', 'группа']:
            setting["group"] = item[1]
    s = json.dumps(setting, ensure_ascii=False)
    if 'settings' not in os.listdir(os.getcwd()):
        os.mkdir("{}/{}".format(os.getcwd(), 'settings'))
    file_name = "{}/settings/{}.json".format(os.getcwd(), message.from_id)
    try:
        file = open(file_name, mode='w', encoding="UTF-8")
        file.write(s)
        file.close()
        text = "Cохранено"
    except FileExistsError:
        text = "Произошла ошибка, настройки уже существуют, вы можете их обновить:\n" \
               "Обновить настройку <имя настройки>: <значение>\n" \
               "Доступные настройки: группа\n" \
               "Или\nОбновить настройки:\n и каждую настройку с новой строки с значением в  формате как указано выше"
    if message.from_id in settings.admins:
        await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main_admin, ensure_ascii=False))
    else:
        await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main, ensure_ascii=False))


@plugin.on_startswith_text("Update setting", "Обновить настройку")
async def update_setting(message, attachments, env):
    try:
        file_name = "{}/settings/{}.json".format(os.getcwd(), message.from_id)
        file = open(file_name, encoding="UTF-8", mode="r")
        now_setting = file.read()
        now_settings = json.loads(now_setting)
        file.close()
        setting = {
            "group": now_settings['group']
        }
        s = env.body.strip().split(': ')
        if s[0] in ['group', 'группа']:
            setting["group"] = s[1]
        s = json.dumps(setting, ensure_ascii=False)
        file = open(file_name, encoding="UTF-8", mode="w")
        file.write(s)
        file.close()
        text = "настройки были сменены\nс {}\nна {}".format(now_setting, s)
    except FileNotFoundError:
        text = "Произошла ошибка, настроек нет, вы можете настройть:\n" \
               "Сохранить настройки\n" \
               "группа*: <группа>\n" \
               "p.s. все вводить одним сообщением, недопуская ошибок, настройки в любом порядке\n" \
               "* - обязательный параметр"
    if message.from_id in settings.admins:
        await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main_admin, ensure_ascii=False))
    else:
        await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main, ensure_ascii=False))


@plugin.on_startswith_text("Update settings", "Обновить настройки")
async def update_settings(message, attachments, env):
    try:
        file_name = "{}/settings/{}.json".format(os.getcwd(), message.from_id)
        file = open(file_name, encoding="UTF-8", mode="r")
        now_setting = file.read()
        now_settings = json.loads(now_setting)
        file.close()
        setting = {
            "group": now_settings['group']
        }
        s = [item.strip().split(": ") for item in env.body.split('\n')]
        for item in s:
            if item[0] in ['group', 'группа']:
                setting["group"] = item[1]
        s = json.dumps(setting, ensure_ascii=False)
        file = open(file_name, encoding="UTF-8", mode="w")
        file.write(s)
        file.close()
        text = "настройки были сменены\nс {}\nна {}".format(now_setting, s)
    except FileNotFoundError:
        text = "Произошла ошибка, настроек нет, вы можете настройть:\n" \
               "Сохранить настройки\n" \
               "группа*: <группа>\n" \
               "p.s. все вводить одним сообщением, недопуская ошибок, настройки в любом порядке\n" \
               "* - обязательный параметр"
    if message.from_id in settings.admins:
        await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main_admin, ensure_ascii=False))
    else:
        await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main, ensure_ascii=False))
