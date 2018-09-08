import json

token = 'bf90dcf53ded8e2759b4b799970569c42eee11adad2d0b2f031596bd2e227f9d469df88f7f7e5922cda23'

keyboard = {
    "one_time": False,
    "buttons": [{
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
        }, ]
}
