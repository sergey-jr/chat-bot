import json

from kutana import Plugin
import settings

plugin = Plugin(name="меню")


@plugin.on_text("меню", "menu", "назад", "back")
async def help_me(message, attachments, env):
    await env.reply('&#13;', keyboard=json.dumps(settings.keyboard, ensure_ascii=False))
