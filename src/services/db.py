# db/base.py
from abc import ABC, abstractmethod

class BaseDB(ABC):
    @abstractmethod
    def execute(self, sql, params=None):
        """Run a statement that modifies data (INSERT/UPDATE/DELETE)"""
        pass

    @abstractmethod
    def query(self, sql, params=None):
        """Run a statement that fetches data (SELECT)"""
        pass

    @abstractmethod
    async def log_bot_message(chat_id, text, msg_type="text"):
        pass

    @abstractmethod
    def log_user_message(chat_id, user_id, username, message_content, msg_type, reply_to, forwarded_from):
        pass

    @abstractmethod
    def update_row(self, query: str):
        pass

    @abstractmethod
    def search_item(self, data: dict):
        pass

    @abstractmethod
    def all_items(self):
        pass
