import logging

from analyzer.base_analyzer import BaseAnalyzer


class OkxSellAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_okx_sell'
        self.logger = logging.getLogger('OkxSellAnalyzer')
        super().__init__()
