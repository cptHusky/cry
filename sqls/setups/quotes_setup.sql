drop table quotes;

create table if not exists quotes
(
    id          serial
        primary key,
    symbol      varchar(50) not null,
    platform_id int not null
        references platforms(id),
    is_buy      bool not null,
    price       float not null,
    volume      float not null,
    timestamp   timestamp not null
);
