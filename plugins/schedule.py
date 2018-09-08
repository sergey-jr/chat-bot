import json

from kutana import Plugin

plugin = Plugin(name="Расписание")

submenu = {
    "one_time": False,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Расписание на сегодня"
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Расписание на завтра"
                },
                "color": "default"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"3\"}",
                    "label": "Расписание на понедельник"
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"4\"}",
                    "label": "Расписание на вторник"
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"5\"}",
                    "label": "Расписание на среду"
                },
                "color": "default"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"6\"}",
                    "label": "Расписание на четверг"
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"7\"}",
                    "label": "Расписание на пятницу"
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"8\"}",
                    "label": "Расписание на субботу"
                },
                "color": "default"
            }
        ],
        {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"9\"}",
                "label": "Назад"
            },
            "color": "primary"
        }
    ]
}


@plugin.on_text("Расписание")
async def schedule_submenu(message, attachments, env):
    await env.reply('', keyboard=json.dumps(submenu, ensure_ascii=False))


@plugin.on_startswith_text("расписание", "schedule")
async def schedule(message, attachments, env):
    await env.reply('')
