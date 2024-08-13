import logging

from analyzer.base_analyzer import BaseAnalyzer


class CoinbaseSellAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_coinbase_sell'
        self.logger = logging.getLogger('CoinbaseSellAnalyzer')
        super().__init__()
