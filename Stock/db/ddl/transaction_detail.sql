-- 成交时间	成交价格	价格变动	成交量(手)	成交额(元)	性质
-- There is no primary key for this table
create table dw.transaction_detail(
  stock_id varchar(6) not null,
  date date not null,
  time varchar(8) not null,
  trans_price decimal(12,4),
  price_change decimal(12,4),
  volume decimal(22,2), --round-lot
  amount decimal(22,2), --yuan, NOT 10 thansand yuan
  buy_sell integer, -- 1:buy, 2:sell, 3:neutral
  source varchar(16)
);
alter table dw.transaction_detail add constraint fk_buy_sell foreign key(buy_sell) references dw.dim_buy_sell(id);
