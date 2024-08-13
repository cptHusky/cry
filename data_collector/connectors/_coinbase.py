"""Коннектор к Coinbase"""
import json
from datetime import datetime

from data_collector.core.base_connector import BaseConnector
from data_collector.core.models import QuoteData


class CoinbaseConnector(BaseConnector):
    """Коннектор к Coinbase"""
    def __init__(self):
        super().__init__("wss://advanced-trade-ws.coinbase.com", 'coinbase')

    async def subscribe_to_market_data(self, symbol: str):
        """Подписаться на рыночные данные."""
        subscribe_message = json.dumps({
            "type": "subscribe",
            "channels": [{"name": "ticker", "product_ids": [symbol]}]
        })
        await self.websocket.send(subscribe_message)
        self.logger.info("Subscribed to market data for %s", symbol)

    async def unsubscribe_from_market_data(self, symbol: str):
        """Отписаться от рыночных данных."""
        unsubscribe_message = json.dumps({
            "type": "unsubscribe",
            "channels": [{"name": "ticker", "product_ids": [symbol]}]
        })
        await self.websocket.send(unsubscribe_message)
        self.logger.info("Unsubscribed from market data for %s", symbol)

    async def on_message(self, message: str):
        """Асинхронная обработка входящих сообщений."""
        data = json.loads(message)
        if data['type'] == 'ticker' and 'price' in data and 'volume_24h' in data:
            market_data = MarketData(
                exchange="Coinbase",
                symbol=data['product_id'],
                price=float(data['price']),
                volume=float(data['volume_24h']),
                timestamp=datetime.now()
            )
            self.logger.info("MarketData received: %s", market_data)
        else:
            self.logger.debug("Received message: %s", data)
