from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker

from params import CACHE_DATABASE_PARAMS


class QuotesCleaner:
    def __init__(self):
        self.engine = create_engine(CACHE_DATABASE_PARAMS)
        configured_session = sessionmaker(bind=self.engine)
        configured_session()

    def clean(self):
        cleaning_sql = text("""
                            TRUNCATE binance_buy, binance_sell, 
                                     bitfinex_buy, bitfinex_sell,
                                     bybit_buy, bybit_sell,
                                     coinbase_buy, coinbase_sell,
                                     huobi_buy, huobi_sell,
                                     kraken_buy, kraken_sell,
                                     okx_buy, okx_sell RESTART IDENTITY CASCADE;
                            """)

        with self.engine.connect() as connection:
            connection.execute(cleaning_sql)
            connection.commit()
            print("B/S tables cleaned")


cleaner = QuotesCleaner()
cleaner.clean()
