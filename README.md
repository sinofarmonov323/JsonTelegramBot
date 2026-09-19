# JsonBot

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

## you can generate code to osonbot library itself (supports only osonbot library, and can not generate fully)
```python
from JSONTelegramBot import JsonBot

JsonBot("token", {
    "messages": {
        "/start": {"response": "hello *{first_name}*", "parse_mode": "MarkdownV2"},
        "/help": {"response": "Hello how can i help you"}
    }
}).generate_code(library="osonbot", file="main.py")
```

## Handling Inline Messages
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

# Done for now
