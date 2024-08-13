"""Коннектор к Binance"""
import json
import logging
from datetime import datetime

from data_collector.core import BaseConnector
from data_collector.core.models import QuoteData
from data_collector.params import BINANCE_WS_URL


class BinanceConnector(BaseConnector):
    """Коннектор к Binance"""

    platform_name: str = "binance"

    def __init__(self):
        self.logger = logging.getLogger('BinanceConnector')
        self.logger.setLevel(logging.DEBUG)
        super().__init__(BINANCE_WS_URL)
        self.channel = 'binance'

    async def subscribe_to_market_data(self, symbol: str):
        """Подписаться на поток тикера для указанной торговой пары."""
        subscribe_message = json.dumps({
            "method": "SUBSCRIBE",
            "params": [
                f"{symbol}@depth@100ms"
            ],
        })
        await self.websocket.send(subscribe_message)
        self.logger.info("Subscribed to %s", symbol)

    async def unsubscribe_from_market_data(self, symbol: str):
        """Отписаться от потока тикера для указанной торговой пары."""
        unsubscribe_message = json.dumps({
            "method": "UNSUBSCRIBE",
            "params": [
                f"{symbol}@depth@100ms"
            ],
        })
        await self.websocket.send(unsubscribe_message)
        self.logger.info("Unsubscribed from %s", symbol)

    async def on_message(self, message: str):
        """Обработка входящего сообщения."""
        self.logger.debug("Received message: %s", message)
        data = json.loads(message)
        if 'e' in data and data['e'] == 'depthUpdate':
            symbol = data['s']
            pipe = self.redis.pipeline()
            for buy in data['b']:
                quote_data = QuoteData(
                    symbol=symbol,
                    price=float(buy[0]),
                    volume=float(buy[1]),
                    timestamp=datetime.fromtimestamp(data['E'] / 1000.0).isoformat()
                )
                pipe.lpush('binance_buy', json.dumps(quote_data.__dict__))
            for sell in data['a']:
                quote_data = QuoteData(
                    symbol=symbol,
                    price=float(sell[0]),
                    volume=float(sell[1]),
                    timestamp=datetime.fromtimestamp(data['E'] / 1000.0).isoformat()
                )
                pipe.lpush('binance_sell', json.dumps(quote_data.__dict__))
            self.logger.debug("Finished processing message")
            await pipe.execute()
            # await self.redis.publish(self.channel, 'new_data')
