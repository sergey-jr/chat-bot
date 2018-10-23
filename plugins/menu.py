import json

from kutana import Plugin
import keyboards, settings

plugin = Plugin(name="меню")


@plugin.on_text("меню", "menu", "назад", "back")
async def help_me(message, attachments, env):
    if message.from_id in settings.admins:
        await env.reply('Меню', keyboard=json.dumps(keyboards.keyboard_main_admin, ensure_ascii=False))
    else:
        await env.reply('Меню', keyboard=json.dumps(keyboards.keyboard_main, ensure_ascii=False))
