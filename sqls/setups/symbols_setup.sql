create table if not exists symbols
(
    id       serial
        primary key,
    name     varchar,
    binance  varchar,
    bitfinex varchar,
    bybit    varchar,
    coinbase varchar,
    huobi    varchar,
    kraken   varchar,
    okx      varchar
);