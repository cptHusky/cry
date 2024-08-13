import logging

from analyzer.base_analyzer import BaseAnalyzer


class HuobiBuyAnalyzer(BaseAnalyzer):
    def __init__(self):
        self.notification_name = 'new_huobi_buy'
        self.logger = logging.getLogger('HuobiBuyAnalyzer')
        super().__init__()
