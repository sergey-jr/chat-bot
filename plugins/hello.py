import json

from kutana import Plugin
import settings

plugin = Plugin(name="привет")


@plugin.on_text("привет", "hallo")
async def hello(message, attachments, env):
    user = await env.request("users.get", user_ids=[message.from_id], name_case="Nom")
    user = user.response[0]
    text = 'Привет, {}!Я чат-бот для студентов. \
                    Могу показать расписание на любой день недели или неделю.'.format(user['first_name'])
    await env.reply(text, keyboard=json.dumps(settings.keyboard, ensure_ascii=False))
