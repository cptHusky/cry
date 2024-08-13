"""Коннектор к Huobi"""
import gzip
import json
import logging
from datetime import datetime
from io import BytesIO

from data_collector.core import BaseConnector
from data_collector.core.models import QuoteData
from data_collector.params import HUOBI_WS_URL


class HuobiConnector(BaseConnector):
    """Коннектор к Huobi"""

    platform_name: str = "huobi"

    def __init__(self):
        self.logger = logging.getLogger('HuobiConnector')
        self.logger.setLevel(logging.DEBUG)
        super().__init__(HUOBI_WS_URL)
        self.channel = 'huobi'

    async def subscribe_to_market_data(self, symbol: str):
        subscribe_message = json.dumps({
            "sub": f"market.{symbol}.depth.step0",
            "id": f"id_{symbol}"
        })
        await self.websocket.send(subscribe_message)
        self.logger.info("Subscribed to market data for %s", symbol)

    async def unsubscribe_from_market_data(self, symbol: str): ...
    #     formatted_symbol = symbol.lower().replace("/", "")
    #     if formatted_symbol in self.subscriptions:
    #         unsubscribe_message = json.dumps({
    #             "unsub": f"market.{formatted_symbol}.trade.detail",
    #             "id": f"id_{formatted_symbol}"
    #         })
    #         await self.websocket.send(unsubscribe_message)
    #         self.subscriptions.remove(formatted_symbol)
    #         self.logger.info("Unsubscribed from market data for %s", symbol)

    async def on_message(self, message: str):
        # noinspection PyTypeChecker
        with gzip.GzipFile(fileobj=BytesIO(message)) as decompressed_file:
            decompressed_message = decompressed_file.read()

        data = json.loads(decompressed_message)

        if 'ping' in data:
            await self.websocket.send(json.dumps({"pong": data['ping']}))
        elif 'ch' in data and 'tick' in data:
            channel = data['ch'].split(".")
            if len(channel) == 4 and channel[2] == "depth":
                symbol = channel[1].upper()
                pipe = self.redis.pipeline()
                bids = data['tick']['bids']
                asks = data['tick']['asks']
                for bid in bids:
                    quote_data = QuoteData(
                        symbol=symbol,
                        price=float(bid[0]),
                        volume=float(bid[1]),
                        timestamp=datetime.fromtimestamp(data['ts'] / 1000.0).isoformat()
                    )
                    pipe.lpush('huobi_buy', json.dumps(quote_data.__dict__))
                for ask in asks:
                    quote_data = QuoteData(
                        symbol=symbol,
                        price=float(ask[0]),
                        volume=float(ask[1]),
                        timestamp=datetime.fromtimestamp(data['ts'] / 1000.0).isoformat()
                    )

                    pipe.lpush('huobi_sell', json.dumps(quote_data.__dict__))
                self.logger.info("Market data update: %s", quote_data)
                await pipe.execute()

        else:
            self.logger.debug("Received message: %s", data)

    async def reconnect(self):
        """Переподключение"""
        if self.websocket:
            await self.websocket.close()
        await self.connect()
        for symbol in self.subscriptions:
            await self.subscribe_to_market_data(symbol)
