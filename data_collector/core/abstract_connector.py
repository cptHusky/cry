"""Абстрактный коннектор"""
from abc import ABC, abstractmethod


class AbstractConnector(ABC):
    """Абстрактный коннектор"""
    def __init__(self, uri: str):
        self.uri = uri

    @abstractmethod
    async def connect(self):
        """Установить соединение с WebSocket."""

    @abstractmethod
    async def disconnect(self):
        """Разорвать соединение с WebSocket."""

    @abstractmethod
    async def on_message(self, message: str):
        """Обработать сообщение, полученное от WebSocket."""
