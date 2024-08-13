import logging

from analyzer.base_analyzer import BaseAnalyzer


class HuobiSellAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_huobi_sell'
        self.logger = logging.getLogger('HuobiSellAnalyzer')
        super().__init__()
