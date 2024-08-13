"""Коннектор к Bybit"""
import json
import logging
from datetime import datetime

from data_collector.core import BaseConnector
from data_collector.core.models import QuoteData
from data_collector.params import BYBIT_WS_URL


class BybitConnector(BaseConnector):
    """Коннектор к Bybit"""

    platform_name: str = "bybit"

    def __init__(self):
        self.logger = logging.getLogger('BybitConnector')
        self.logger.setLevel(logging.DEBUG)
        super().__init__(BYBIT_WS_URL)
        self.channel = 'bybit'

    async def subscribe_to_market_data(self, symbol: str):
        """Подписаться на поток тикера для указанной торговой пары на Bybit."""

        subscribe_message = json.dumps({
            "category": "spot",
            "args": [f"tickers.{symbol}"]
        })

        await self.websocket.send(subscribe_message)
        self.logger.info("Subscribed to %s ticker", symbol)

    async def unsubscribe_from_market_data(self, symbol: str):
        unsubscribe_message = json.dumps({
            "op": "unsubscribe",
            "args": [f"tickers.{symbol}"]
        })
        await self.websocket.send(unsubscribe_message)
        self.logger.info("Unsubscribed from %s ticker", symbol)

    async def on_message(self, message: str):
        """Обработка входящего сообщения."""
        data = json.loads(message)
        if 'topic' in data and 'data' in data:
            market_data = QuoteData(
                exchange="Bybit",
                symbol=data['data']['symbol'],
                price=float(data['data']['lastPrice']),
                volume=float(data['data']['volume24h']),
                timestamp=datetime.now()
            )
            self.logger.info("MarketData received: %s", market_data)
        else:
            self.logger.warning("Received message with unexpected format or without necessary data:%s", data)
