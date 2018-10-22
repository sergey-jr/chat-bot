import json

from kutana import Plugin
import keyboards

plugin = Plugin(name="меню")


@plugin.on_text("меню", "menu", "назад", "back")
async def help_me(message, attachments, env):
    await env.reply('Меню', keyboard=json.dumps(keyboards.keyboard_main, ensure_ascii=False))
