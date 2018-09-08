from kutana import Plugin

plugin = Plugin(name="Скажи")


@plugin.on_startswith_text("скажи", "say")
async def on_echo(message, attachments, env):
    await env.reply("{}".format(env.body))
