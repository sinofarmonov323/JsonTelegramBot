# JsonTelegramBot

Build lightweight **Telegram bots from JSON configuration** in Python. JsonTelegramBot
is a configuration-driven wrapper around

## Features

- Configure Telegram bot handlers with a Python dictionary or a JSON file.
- Reply to commands and text messages without writing repetitive handler code.
- Add an explicit `"*"` wildcard response for otherwise unhandled text.
- Handle inline callback data with `inline-messages`.
- Send a configured response to a specific Telegram user ID.
- Generate equivalent `osonbot` Python code.
- MIT licensed and compatible with Python 3.10 and newer.

# Installation
```shell
pip install json-telegram-bot
```

# Usage
```python
from JSONTelegramBot import JsonBot

JsonBot("token", {
    "messages": {
        "/start": {"response": "hello *{first_name}*", "parse_mode": "MarkdownV2"},
        "/help": {"response": "Hello how can i help you"}
    }
}).run()
```

## Generate osonbot code

Generate standalone Python code for the supported `osonbot` library:
```python
from JSONTelegramBot import JsonBot

JsonBot("token", {
    "messages": {
        "/start": {"response": "hello *{first_name}*", "parse_mode": "MarkdownV2"},
        "/help": {"response": "Hello how can i help you"}
    }
}).generate_code(library="osonbot", file="main.py")
```

## Handling inline callback messages
```python
from JSONTelegramBot import JsonBot

JsonBot("token", {
    "inline-messages": {
        "callback_data1": {"response": "you clicked the first inline button"},
        "callback_data2": {"response": "you clicked the sedond inline button"}
    }
}).run()
```

## Send message to specific user by their Telegram ID
```python
from JSONTelegramBot import JsonBot

JsonBot("token", {
    "messages": {
        "/start": {"response": "hello *{first_name}*", "parse_mode": "MarkdownV2"},
        "/send": {"id": 123456789, "response": "This is a message for a specific user"}
    }
}).run()
```

## License

JsonTelegramBot is released under the [MIT License](LICENSE).
