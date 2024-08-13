import logging

from analyzer.base_analyzer import BaseAnalyzer


class BitfinexBuyAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_bitfinex_buy'
        self.logger = logging.getLogger('BitfinexBuyAnalyzer')
        super().__init__()
