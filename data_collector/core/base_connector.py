"""Базовый коннектор"""
import json
from abc import abstractmethod
from logging import Logger

import websockets
from redis.asyncio import Redis

from data_collector.core.abstract_connector import AbstractConnector
from params import CACHE_DATABASE_PARAMS


class BaseConnector(AbstractConnector):
    """Базовый коннектор"""
    logger: Logger

    def __init__(self, uri: str):
        super().__init__(uri)
        self.redis = self._get_db_client()

    async def connect(self):
        """Асинхронное установление соединения с WebSocket."""
        try:
            a = 1
            self.websocket = await websockets.connect(self.uri)
            self.logger.info("Connected to %s", self.uri)
        except Exception as e:
            self.logger.error("Failed to connect to %s: %s", self.uri, e)

    async def disconnect(self):
        """Асинхронное отключение от WebSocket."""
        if self.websocket:
            try:
                await self.websocket.close()
                self.logger.info("Disconnected")
            except Exception as e:
                self.logger.error("Failed to disconnect: %s, killing client", e)
            finally:
                self.websocket = None
        else:
            self.logger.error("No client connected to %s", self.uri)

    async def listen(self):
        """Слушать сообщения от WebSocket и обрабатывать их."""
        while self.websocket:
            try:
                async for message in self.websocket:
                    await self.on_message(message)
            except Exception as e:
                self.logger.error("Error while listening: %s", e)

    @abstractmethod
    async def subscribe_to_market_data(self, symbol: str):
        """Подписаться на рыночные данные для указанной торговой пары."""

    @abstractmethod
    async def unsubscribe_from_market_data(self, symbol: str):
        """Отписаться от рыночных данных для указанной торговой пары."""

    async def on_message(self, message: str):
        """Базовая обработка входящего сообщения."""

        data = json.loads(message)

        self.logger.info("No 'on_message' configured in subclass. Message received: %s", data)

    async def run(self, symbols):
        """Запускает коннектор. Подключается, слушает."""
        await self.connect()
        for symbol in symbols:
            await self.subscribe_to_market_data(symbol=symbol)

        try:
            await self.listen()
        except KeyboardInterrupt:
            # await self.unsubscribe_from_market_data(symbol)
            await self.disconnect()
        except Exception as e:

            print(f"An error occurred: {e}")
            await self.disconnect()

    def report_unknown_message(self, data):
        """Лог о неизвестном сообщении"""
        self.logger.warning("Received non-ticker message or unrecognized format: %s", data)

    def _get_db_client(self):
        redis_client = Redis(**CACHE_DATABASE_PARAMS)
        self.logger.info("Connected to Redis: %s", CACHE_DATABASE_PARAMS)
        return redis_client
