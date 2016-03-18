
create table dw.dim_buy_sell(
  id integer not null,
  name varchar(8), -- 1:buy, 2:sell, 3:neutral
  primary key(id)
);

insert into dw.dim_buy_sell values
(1, '买盘'),
(2, '卖盘'),
(3, '中性盘');