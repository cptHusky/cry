import logging

from analyzer.base_analyzer import BaseAnalyzer


class OkxBuyAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_okx_buy'
        self.logger = logging.getLogger('OkxBuyAnalyzer')
        super().__init__()
