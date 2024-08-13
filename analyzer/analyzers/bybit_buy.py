import logging

from analyzer.base_analyzer import BaseAnalyzer


class BybitBuyAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_bybit_buy'
        self.logger = logging.getLogger('BybitBuyAnalyzer')
        super().__init__()
