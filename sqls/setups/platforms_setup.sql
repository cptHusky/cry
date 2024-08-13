create table if not exists platforms
(
    id   serial
        primary key,
    name varchar(255) not null
);


INSERT INTO platforms (id, name) VALUES
(1, 'binance'),
(2, 'bitfinex'),
(3, 'bybit'),
(4, 'coinbase'),
(5, 'huobi'),
(6, 'kraken'),
(7, 'okx')
ON CONFLICT (id) DO NOTHING;