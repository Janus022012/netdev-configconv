from typing import Any, Dict

class CustomError(Exception):
    ja_message: str = ""

    def __init__(self, message_items: Dict[str, Any]):
        self.message_items = message_items

    def get_ja_message(self) -> str:
            return self.ja_message.format_map(self.message_items)
    