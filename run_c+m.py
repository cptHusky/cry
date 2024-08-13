import asyncio
import logging
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from data_collector.connectors import *
from logger_config import LOGGER_CONFIG
from memory_maintainer import RedisToPGTransfer
from params import VALUES_DATABASE_PARAMS

logging.basicConfig(**LOGGER_CONFIG)

run_params = {
    # "use_proxy": True,
    "clean_log_on_start": True,
}


PROXY_CONFIG = '192.111.129.145:16894'


class ConnectorsApp:
    connectors = [
        BinanceConnector,
        # BybitConnector,
        # HuobiConnector,
        # OkxConnector,
        # -------------
        # BitfinexConnector,
        # CoinbaseConnector,
        # KrakenConnector,
    ]

    maintainers = [
        RedisToPGTransfer(),
    ]

    def __init__(self):
        print('ConnectorsApp started')
        self.engine = create_engine(VALUES_DATABASE_PARAMS)
        configured_session = sessionmaker(bind=self.engine)
        configured_session()

    async def run(self,
                  use_proxy: bool = False,
                  clean_log_on_start: bool = False):
        if clean_log_on_start:
            with open("log.log", 'w') as f:
                f.close()
        print('Connectors starting:')
        for connector in self.connectors:
            print(connector.platform_name)
        print('Maintainers starting:')
        for maintainer in self.maintainers:
            print(maintainer.__class__.__name__)
        if use_proxy:
            os.environ['HTTP_PROXY'] = f"socks5://{PROXY_CONFIG}"
            os.environ['HTTPS_PROXY'] = f"socks5://{PROXY_CONFIG}"
        else:
            os.environ.pop('HTTP_PROXY', None)
            os.environ.pop('HTTPS_PROXY', None)

        tasks = []
        for _c in self.connectors:
            c = _c()
            with self.engine.connect() as connection:
                sql = text(
                    f"SELECT {c.platform_name} FROM symbols WHERE {c.platform_name} IS NOT NULL;")
                result = connection.execute(sql).all()
                symbols = []
                for row in result:
                    symbols.append(row[0])

                c_task = c.run(symbols=symbols)
                tasks.append(c_task)

        for m in self.maintainers:
            m_task = m.run()
            tasks.append(m_task)
        await asyncio.gather(*tasks)


app = ConnectorsApp()
asyncio.run(app.run(**run_params))
