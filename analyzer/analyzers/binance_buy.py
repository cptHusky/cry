import logging

from analyzer.base_analyzer import BaseAnalyzer


class BinanceBuyAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_binance_buy'
        self.logger = logging.getLogger('BinanceBuyAnalyzer')
        super().__init__()
