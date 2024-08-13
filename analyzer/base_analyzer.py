"""Базовый анализатор. Ждёт обновления и вызывает брокер для торговли"""
import logging

import psycopg2
import select

from params import CACHE_DATABASE_PARAMS


class BaseAnalyzer:
    notification_name: str

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        # TODO: INFO
        self.logger.setLevel(logging.DEBUG)

    async def process_updates(self):
        # self.logger.info("Started")
        # conn = psycopg2.connect(DATABASE_CONN_PARAMS)
        # self.logger.info('Connected to %s', DATABASE_CONN_PARAMS)
        # conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        #
        # cur = conn.cursor()
        # cur.execute(f'LISTEN {self.notification_name};')

        sub = self.redis.pubsub()

        self.logger.info("Waiting for notifications on channel %s", self.notification_name)
        try:
            while True:
                select.select([conn], [], [])
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    self.logger.debug("Got NOTIFY: %s %s %s", notify.pid, notify.channel, notify.payload)
                    # trading and deciding logic implemented here
        finally:
            self.logger.info("Shutting down")
            cur.close()
            self.logger.info("Cursor closed")
            conn.close()
            self.logger.info("Connection closed")
