"""Коннектор к OKX"""
import json
import logging
from datetime import datetime

from data_collector.core import BaseConnector
from data_collector.params import OKX_WS_URL
from mappings.symbols import okx_symbols_mapping


class OkxConnector(BaseConnector):
    """Коннектор к OKX"""
    symbol: str

    platform_name: str = "binance"

    def __init__(self):
        super().__init__(OKX_WS_URL)
        self.logger = logging.getLogger('OkxConnector')

    async def subscribe_to_market_data(self, symbol: str):
        """Подписаться на обновления рыночных данных для указанной торговой пары."""
        self.symbol = symbol
        subscribe_message = json.dumps({
            "op": "subscribe",
            "args": [{
                "channel": "books5",
                "instId": self.symbol
            }]
        })
        await self.websocket.send(subscribe_message)
        self.logger.info("Attempted to subscribe to market data for %s", self.symbol)

    async def unsubscribe_from_market_data(self, symbol: str):
        """Отписаться от обновлений рыночных данных для указанной торговой пары."""
        unsubscribe_message = json.dumps({
            "op": "unsubscribe",
            "args": [{
                "channel": "books5",
                "instId": self.symbol
            }]
        })
        await self.websocket.send(unsubscribe_message)
        self.logger.info("Attempted to unsubscribe from market data for %s", symbol)

    async def on_message(self, message):
        data = json.loads(message)
        if data.get('event'):
            if data['event'] == 'subscribe':
                self.logger.info("Subscribed successfully")
            else:
                self.logger.warning("Error occurred: %s", data['msg'])
        elif 'arg' in data and 'data' in data:
            symbol_id = okx_symbols_mapping[data['arg']['instId']]
            if data['arg']['channel'] == 'books5':
                for buy in data['data'][0]['bids']:
                    self.redis.add(OkxBuy(
                        symbol_id=symbol_id,
                        price=buy[0],
                        volume=buy[1],
                        timestamp=datetime.fromtimestamp(float(data['data'][0]['ts']) / 1000.0)
                    ))
                for sell in data['data'][0]['asks']:
                    self.redis.add(OkxSell(
                        symbol_id=symbol_id,
                        price=sell[0],
                        volume=sell[1],
                        timestamp=datetime.fromtimestamp(float(data['data'][0]['ts']) / 1000.0)
                    ))
                self.redis.commit()
                self.logger.debug("MarketData received: %s", data)
        else:
            self.report_unknown_message(data)
