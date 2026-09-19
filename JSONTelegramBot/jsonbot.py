import json
from collections.abc import Mapping
from os import PathLike
from pathlib import Path
from typing import Any

from osonbot import Bot, InlineKeyboardButton, KeyboardButton, URLKeyboardButton


class JsonTelegramBot(Bot):
    def __init__(
        self,
        token: str,
        configure: str | PathLike[str] | Mapping[str, Any],
    ):
        if not isinstance(token, str) or not token.strip():
            raise ValueError("token must be a non-empty string")

        self.token = token
        super().__init__(token, auto_db=False)

        if isinstance(configure, (str, PathLike)):
            with Path(configure).open("r", encoding="utf-8") as config_file:
                configure = json.load(config_file)

        if not isinstance(configure, Mapping):
            raise TypeError("configure must be a mapping or a path to a JSON object")

        self.configure = dict(configure)
        self._validate_config()

    def _validate_config(self) -> None:
        for section_name in ("messages", "inline-messages"):
            section = self.configure.get(section_name, {})
            if not isinstance(section, Mapping):
                raise TypeError(f"{section_name} must be a mapping")

            for condition, data in section.items():
                if not isinstance(condition, str) or not condition:
                    raise TypeError(f"{section_name} conditions must be non-empty strings")
                if not isinstance(data, Mapping):
                    raise TypeError(
                        f"{section_name}[{condition!r}] must be a mapping"
                    )
                if section_name == "messages" and "response" not in data and "text" not in data:
                    raise ValueError(
                        f"messages[{condition!r}] must define 'response' or 'text'"
                    )
                if section_name == "inline_messages" and "response" not in data:
                    raise ValueError(
                        f"inline_messages[{condition!r}] must define 'response'"
                    )

    def setter(self):
        for condition, data in self.configure.get("messages", {}).items():
            response = data.get("response", data.get("text", ""))
            parse_mode = data.get("parse_mode")
            buttons = data.get("reply_markup")
            chat_id = data.get("id")

            if chat_id is not None:
                def send_to_id(
                    message,
                    chat_id=chat_id,
                    response=response,
                    parse_mode=parse_mode,
                    buttons=buttons,
                ):
                    return self.send_message(
                        chat_id=chat_id,
                        text=response,
                        parse_mode=parse_mode,
                        reply_markup=buttons,
                    )

                self.when(
                    condition=condition,
                    text=send_to_id,
                    parse_mode=parse_mode,
                    reply_markup=buttons,
                )
            else:
                self.when(
                    condition=condition,
                    text=response,
                    parse_mode=parse_mode,
                    reply_markup=buttons,
                )

        for condition, data in self.configure.get("inline-messages", {}).items():
            self.c_when(
                condition=condition,
                text=data.get("response", ""),
                parse_mode=data.get("parse_mode"),
                reply_markup=data.get("reply_markup"),
            )

        if self.configure.get("background-task") is not None:
            self.configure.get('background-task')(self)

    def generate_code(self, library: str, file: str | PathLike[str]):
        if library != "osonbot":
            raise ValueError("JsonBot.generate_code only supports the 'osonbot' library")

        lines = [
            "from osonbot import Bot",
            "",
            f"bot = Bot({self.token!r})",
            "",
        ]

        for condition, data in self.configure.get("messages", {}).items():
            response = data.get("response", data.get("text", ""))
            parse_mode = data.get("parse_mode")
            buttons = data.get("reply_markup")
            chat_id = data.get("id")

            if chat_id is not None:
                lines.append(
                    f"bot.when({condition!r}, "
                    f"lambda message, chat_id={chat_id!r}: "
                    f"bot.send_message(chat_id=chat_id, text={response!r}, "
                    f"parse_mode={parse_mode!r}, reply_markup={buttons!r}))"
                )
            else:
                lines.append(
                    f"bot.when({condition!r}, {response!r}, "
                    f"parse_mode={parse_mode!r}, reply_markup={buttons!r})"
                )

        for condition, data in self.configure.get("inline_messages", {}).items():
            lines.append(
                f"bot.c_when({condition!r}, {data.get('response', '')!r}, "
                f"parse_mode={data.get('parse_mode')!r}, "
                f"reply_markup={data.get('reply_markup')!r})"
            )

        lines.extend(["", "bot.run()", ""])
        code = "\n".join(lines)
        output_path = Path(file)
        with output_path.open("w", encoding="utf-8") as generated_file:
            generated_file.write(code)

        self.logger.info("Code generated in %s", output_path)
        return code

    def run(self):
        self.setter()
        return super().run()

    def process_messages(self, message):
        """Process configured text messages, including an explicit wildcard."""
        if "text" not in message:
            return

        text = message.get("text")
        if text in self.handlers:
            return super().process_messages(message)

        wildcard_handler = self.handlers.get("*")
        if wildcard_handler is None:
            return

        # osonbot's fallback is the literal "*" string rather than the
        # configured wildcard handler. Give it the selected handler directly.
        self.handlers[text] = wildcard_handler
        try:
            return super().process_messages(message)
        finally:
            del self.handlers[text]
