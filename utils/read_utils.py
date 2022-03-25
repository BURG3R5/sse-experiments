import json
from os import path
from typing import Any


class ReadUtils:
    @staticmethod
    def read_messages_element() -> dict[str, str]:
        events: list[dict[str, Any]] = []
        messages: dict[str, str] = {}
        if path.exists("documents/export.json"):
            with open("documents/export.json", encoding="utf-8") as file:
                events: list[dict[str, Any]] = json.load(file)["messages"]
        for event in events:
            if event["type"] == "m.room.message":
                try:
                    messages[event["event_id"]] = event["content"]["body"]
                except KeyError:
                    # This just means that the message was redacted
                    pass
        return messages
