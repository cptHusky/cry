import json
import logging
from asyncio import sleep

from sqlalchemy import create_engine, text

import psycopg2
from redis.asyncio import Redis
from sqlalchemy.orm import sessionmaker

from params import CACHE_DATABASE_PARAMS, VALUES_DATABASE_PARAMS

PLATFORMS_MAPPING = {
    "binance": 1,
    "bybit": 3,
    "huobi": 5,
    "okx": 7,
}


class RedisToPGTransfer:
    def __init__(self):
        self.logger = logging.getLogger('MemoryMaintainer')
        self.logger.setLevel(logging.DEBUG)
        self.redis = self._get_redis_client()
        self.engine = create_engine(VALUES_DATABASE_PARAMS)
        configured_session = sessionmaker(bind=self.engine)
        configured_session()
        self.pg_connection = self.engine.connect()

    async def run(self):
        self.logger.debug('mem maintainer start')
        self.logger.setLevel(logging.DEBUG)
        keys = await self.redis.keys()
        batch = 100

        while True:
            for key in keys:
                key = key.decode()
                data = await self.redis.lrange(key, 0, -1)
                if (ld := len(data) - batch) > 0:
                    platform, side = key.split('_')
                    platform_id = self._get_platform_id(platform)
                    is_buy = 'true' if side == 'buy' else 'false'
                    sql = ("INSERT INTO quotes (symbol, platform_id, is_buy, price, volume, timestamp) "
                           "VALUES ")

                    for item in data[:ld]:
                        record = json.loads(item)
                        sql += f"""
                        ('{record['symbol']}', {platform_id}, {is_buy},  '{record['price']}',
                         '{record['volume']}', '{record['timestamp']}'),"""
                    sql = sql[:-1]
                    self.pg_connection.execute(text(sql))
                    self.pg_connection.commit()
                    await self.redis.ltrim(key, ld, -1)
                    self.logger.debug('cleaned %s ltrim, moved %s quotes', key, ld)
            await sleep(2)

    def _get_pg_client(self):
        conn = psycopg2.connect(VALUES_DATABASE_PARAMS)
        self.logger.info("Connected to Redis: %s", CACHE_DATABASE_PARAMS)
        return conn

    def _get_redis_client(self):
        redis_client = Redis(**CACHE_DATABASE_PARAMS)
        self.logger.info("Connected to Redis: %s", CACHE_DATABASE_PARAMS)
        return redis_client

    def _get_platform_id(self, platform_name):
        sql = text(f"SELECT id FROM platforms WHERE name = '{platform_name}'")
        result = self.pg_connection.execute(sql)
        a = 1
        for platform_id in result:
            return platform_id[0]
        # return result['id']
