import json

from kutana import Plugin
import keyboards, settings

plugin = Plugin(name="Админка")


@plugin.on_text("Админка", "admin")
async def admin(message, attachments, env):
    if message.from_id in settings.admins:
        text = 'ok'
    else:
        text = 'Доступ запрещен'
    await env.reply(text, keyboard=json.dumps(keyboards.keyboard_main_admin, ensure_ascii=False))