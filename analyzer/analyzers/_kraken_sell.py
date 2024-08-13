import logging

from analyzer.base_analyzer import BaseAnalyzer


class KrakenSellAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_kraken_sell'
        self.logger = logging.getLogger('KrakenSellAnalyzer')
        super().__init__()
