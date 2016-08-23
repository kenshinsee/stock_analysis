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

create table dw.stock_transaction_20160510 ( check ( biz_date >= date '2016-05-10' AND biz_date <= DATE '2016-05-10' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160511 ( check ( biz_date >= date '2016-05-11' AND biz_date <= DATE '2016-05-11' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160512 ( check ( biz_date >= date '2016-05-12' AND biz_date <= DATE '2016-05-12' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160513 ( check ( biz_date >= date '2016-05-13' AND biz_date <= DATE '2016-05-13' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160516 ( check ( biz_date >= date '2016-05-16' AND biz_date <= DATE '2016-05-16' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160517 ( check ( biz_date >= date '2016-05-17' AND biz_date <= DATE '2016-05-17' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160518 ( check ( biz_date >= date '2016-05-18' AND biz_date <= DATE '2016-05-18' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160519 ( check ( biz_date >= date '2016-05-19' AND biz_date <= DATE '2016-05-19' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160520 ( check ( biz_date >= date '2016-05-20' AND biz_date <= DATE '2016-05-20' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160523 ( check ( biz_date >= date '2016-05-23' AND biz_date <= DATE '2016-05-23' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160524 ( check ( biz_date >= date '2016-05-24' AND biz_date <= DATE '2016-05-24' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160525 ( check ( biz_date >= date '2016-05-25' AND biz_date <= DATE '2016-05-25' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160526 ( check ( biz_date >= date '2016-05-26' AND biz_date <= DATE '2016-05-26' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160527 ( check ( biz_date >= date '2016-05-27' AND biz_date <= DATE '2016-05-27' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160530 ( check ( biz_date >= date '2016-05-30' AND biz_date <= DATE '2016-05-30' ) ) INHERITS (dw.stock_transaction);
create table dw.stock_transaction_20160531 ( check ( biz_date >= date '2016-05-31' AND biz_date <= DATE '2016-05-31' ) ) INHERITS (dw.stock_transaction);