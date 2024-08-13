"""Коннектор к Kraken"""
import json
import logging
from datetime import datetime

from data_collector.core import BaseConnector
from mappings.symbols import kraken_symbols_mapping


class KrakenConnector(BaseConnector):
    """Коннектор к Kraken"""
    def __init__(self):
        super().__init__("wss://ws.kraken.com", 'kraken')
        self.subscriptions = {}
        self.logger = logging.getLogger('KrakenConnector')

    async def subscribe_to_market_data(self, symbol: str):
        """Подписаться на тикер определенной торговой пары."""
        subscribe_message = json.dumps({
            "event": "subscribe",
            "pair": [symbol],
            "subscription": {"name": "book"}
        })
        await self.websocket.send(subscribe_message)
        self.logger.info("Attempted to subscribe to market data for %s", symbol)

    async def unsubscribe_from_market_data(self, symbol: str):
        """Отписаться от тикера определенной торговой пары."""
        if symbol in self.subscriptions:
            unsubscribe_message = json.dumps({
                "event": "unsubscribe",
                "pair": [symbol],
                "subscription": {"name": "book"}
            })
            await self.websocket.send(unsubscribe_message)
            self.logger.info("Attempted to unsubscribe from market data for %s", symbol)

    async def on_message(self, message):

        data = json.loads(message)
        if 'event' in data:
            if data['event'] == 'subscriptionStatus' and data['status'] == 'subscribed':
                self.subscriptions[data['pair']] = data['channelID']
                self.logger.info("Subscribed to %s with channelID %s", data['pair'], data['channelID'])
            elif data['event'] == 'subscriptionStatus' and data['status'] == 'unsubscribed':
                del self.subscriptions[data['pair']]
                self.logger.info("Unsubscribed from %s", data['pair'])
        elif self._data_valid(data):
            symbol_id = kraken_symbols_mapping[data[3]]

            buys = data[1].get('b')
            if buys is None:
                buys = data[1].get('bs')
            if buys is not None:
                for buy in buys:
                    self.redis.add(KrakenBuy(
                        symbol_id=symbol_id,
                        price=buy[0],
                        volume=buy[1],
                        timestamp=datetime.fromtimestamp(float(buy[2]))
                    ))
            sells = data[1].get('a')
            if sells is None:
                sells = data[1].get('as')
            if sells is not None:
                for sell in sells:
                    self.redis.add(KrakenSell(
                        symbol_id=symbol_id,
                        price=sell[0],
                        volume=sell[1],
                        timestamp=datetime.fromtimestamp(float(sell[2]))
                    ))
            self.redis.commit()
            self.logger.debug("MarketData received: %s", data)
        else:
            self.report_unknown_message(data)

    @staticmethod
    def _data_valid(data):
        if isinstance(data, list) and 3 < len(data) < 6 and isinstance(data[1], dict) and isinstance(data[1], dict):
            return True
        return False
