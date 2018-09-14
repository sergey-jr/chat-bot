import json

from kutana import Plugin
import settings

plugin = Plugin(name="Помощь")


@plugin.on_text("помощь", "help", "начать", "start")
async def help_me(message, attachments, env):
    text = "Помощь - вывести список доступных команд\n\ " \
           "Расписание на ...(<день недели>, сегодня, завтра, неделю)"
    await env.reply(text, keyboard=json.dumps(settings.keyboard, ensure_ascii=False))
