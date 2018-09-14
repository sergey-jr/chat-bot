from kutana import Plugin
import settings

plugin = Plugin(name="привет")


@plugin.on_text("привет", "hallo")
async def hello(message, attachments, env):
    text = 'Привет, друг!\nЯ чат-бот для студентов. \
                Могу показать расписание на любой день недели или неделю.'
    await env.reply(text)
