import logging

from analyzer.base_analyzer import BaseAnalyzer


class BitfinexSellAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_bitfinex_sell'
        self.logger = logging.getLogger('BitfinexSellAnalyzer')
        super().__init__()
