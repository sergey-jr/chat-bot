import json

from kutana import Plugin
import keyboards, settings

plugin = Plugin(name="начать")


@plugin.on_text("помощь", "help", "начать", "start", "привет", "hallo")
async def help_me(message, attachments, env):
    user = await env.request("users.get", user_ids=[message.from_id], name_case="Nom")
    user = user.response[0]
    text = 'Привет, {}! Я чат-бот для студентов. ' \
           'Могу показать расписание на любой день ' \
           'недели или неделю. \nрасписание на <dd>.<mm>.<yyyy> - ' \
           'расписание на конкретное число' \
        .format(user['first_name'])
    if message.from_id in settings.admins:
        await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main_admin, ensure_ascii=False))
    else:
        await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main, ensure_ascii=False))
