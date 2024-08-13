"""Коннектор к Bitfinex"""
import json
from datetime import datetime

from data_collector.core import BaseConnector
from data_collector.core.models import QuoteData


class BitfinexConnector(BaseConnector):
    """Коннектор к Bitfinex"""
    def __init__(self):
        super().__init__("wss://api-pub.bitfinex.com/ws/2")
        self.channel_ids = {}

    async def subscribe_to_market_data(self, symbol: str):
        """Подписаться на поток тикера для указанной торговой пары на Bitfinex."""
        subscribe_message = json.dumps({
            "event": "subscribe",
            "channel": "ticker",
            "symbol": symbol
        })
        await self.websocket.send(subscribe_message)

        self.logger.info("Subscribing to %s ticker", symbol)

    async def unsubscribe_from_market_data(self, symbol: str):

        chan_id = self.channel_ids.get(symbol)
        if chan_id:
            unsubscribe_message = json.dumps({
                "event": "unsubscribe",
                "chan_id": chan_id
            })
            await self.websocket.send(unsubscribe_message)
            self.logger.info("Unsubscribed from %s ticker", symbol)
        else:
            self.logger.error("No subscription found for %s", symbol)

    async def on_message(self, message: str):
        data = json.loads(message)
        if isinstance(data, list):
            chan_id = data[0]
            if chan_id in self.channel_ids.values() and len(data) > 1 and isinstance(data[1], list):
                ticker_data = data[1]
                price = float(ticker_data[6])
                volume = float(ticker_data[7])
                symbol = [key for key, value in self.channel_ids.items() if value == chan_id][0]
                market_data = MarketData(
                    exchange="Bitfinex",
                    symbol=symbol,
                    price=price,
                    volume=volume,
                    timestamp=datetime.now()
                )
                self.logger.info("MarketData received: %s", market_data)
        else:
            if data.get('event') == 'subscribed' and data.get('channel') == 'ticker':
                self.channel_ids[data['symbol']] = data['chanId']
                self.logger.info("Successfully subscribed to %s ticker with chan_id %s", data['symbol'],data['chanId'])
            elif data.get('event') == 'error':
                self.logger.error("Error: %s", data.get('msg', 'No message'))
