import logging

from analyzer.base_analyzer import BaseAnalyzer


class BybitSellAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_bybit_sell'
        self.logger = logging.getLogger('BybitSellAnalyzer')
        super().__init__()
