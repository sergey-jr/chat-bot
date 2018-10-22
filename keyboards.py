from gettext import gettext as _

schedule_menu = {
    "one_time": False,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": _("Расписание на сегодня")
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": _("Расписание на завтра")
                },
                "color": "default"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"3\"}",
                    "label": _("Расписание на понедельник")
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"4\"}",
                    "label": _("Расписание на вторник")
                },
                "color": "default"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"5\"}",
                    "label": _("Расписание на среду")
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"6\"}",
                    "label": _("Расписание на четверг")
                },
                "color": "default"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"7\"}",
                    "label": _("Расписание на пятницу")
                },
                "color": "default"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"8\"}",
                    "label": _("Расписание на субботу")
                },
                "color": "default"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"9\"}",
                    "label": _("Назад")
                },
                "color": "primary"
            }
        ]
    ]
}

keyboard_main = {
    "one_time": False,
    "buttons": [[
        {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Помощь"
            },
            "color": "default"
        },
        {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Расписание"
            },
            "color": "default"
        }
    ]]
}

keyboard_main_admin = {
    "one_time": False,
    "buttons": [[
        {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Помощь"
            },
            "color": "default"
        },
        {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Расписание"
            },
            "color": "default"
        },
        {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"3\"}",
                "label": "Админка"
            },
            "color": "default"
        }
    ]]
}

settings_menu = {
    "one_time": False,
    "buttons":
        [
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"1\"}",
                        "label": "Назад"
                    },
                    "color": "primary"
                }
            ]
        ]
}
