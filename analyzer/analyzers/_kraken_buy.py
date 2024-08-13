import logging

from analyzer.base_analyzer import BaseAnalyzer


class KrakenBuyAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_kraken_buy'
        self.logger = logging.getLogger('KrakenBuyAnalyzer')
        super().__init__()
