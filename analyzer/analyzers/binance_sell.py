import logging

from analyzer.base_analyzer import BaseAnalyzer


class BinanceSellAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_binance_sell'
        self.logger = logging.getLogger('BinanceSellAnalyzer')
        super().__init__()
