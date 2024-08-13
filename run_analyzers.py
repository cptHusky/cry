import asyncio
import logging

from analyzer.analyzers import *
from logger_config import LOGGER_CONFIG

logging.basicConfig(**LOGGER_CONFIG)


class AnalyzersApp:

    analyzers = [
        BinanceBuyAnalyzer(),
        # BinanceSellAnalyzer(),
        # BitfinexBuyAnalyzer(),
        # BitfinexSellAnalyzer(),
        # BybitBuyAnalyzer(),
        # BybitSellAnalyzer(),
        # CoinbaseBuyAnalyzer(),
        # CoinbaseSellAnalyzer(),
        # HuobiBuyAnalyzer(),
        # HuobiSellAnalyzer(),
        # KrakenBuyAnalyzer(),
        # KrakenSellAnalyzer(),
        # OKXBuyAnalyzer(),
        # OKXSellAnalyzer(),
    ]

    async def run(self):
        print('Analyzers starting:')
        for a in self.analyzers:
            print(a.__class__.__name__)
        analyzer_tasks = []
        for analyzer in self.analyzers:
            a_task = analyzer.process_updates()
            analyzer_tasks.append(a_task)
        await asyncio.gather(*analyzer_tasks)


app = AnalyzersApp()
asyncio.run(app.run())
