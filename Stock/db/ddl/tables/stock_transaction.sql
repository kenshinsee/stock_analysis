-- 成交时间	成交价格	价格变动	成交量(手)	成交额(元)	性质
-- There is no primary key for this table
create table dw.stock_transaction(
  stock_id varchar(6) not null,
  biz_date date not null,
  time varchar(8) not null,
  trans_price decimal(12,4),
  price_change decimal(12,4),
  volume decimal(22,2), --round-lot
  amount decimal(22,2), --yuan, NOT 10 thansand yuan
  buy_sell varchar(32), -- 1:buy, 2:sell, 3:neutral
  source varchar(16)
);
--alter table dw.stock_transaction add constraint fk_buy_sell foreign key(buy_sell) references dw.dim_buy_sell(id);
alter table dw.stock_transaction add constraint fk_stock_id foreign key(stock_id) references dw.dim_stock(id);
create index idx_stock_transaction1 on dw.stock_transaction(biz_date);