import logging

from analyzer.base_analyzer import BaseAnalyzer


class CoinbaseBuyAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_coinbase_buy'
        self.logger = logging.getLogger('CoinbaseBuyAnalyzer')
        super().__init__()
