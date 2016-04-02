-- daily bankuai data
create table dw.bankuai(
  biz_date date not null,
  bankuai_id integer not null,
  rise varchar(16),
  market_value_in_million decimal(12,2),
  turnover_rate decimal(5,2),
  num_of_rise integer,
  num_of_drop integer,
  leading_stock_id varchar(6),
  rise_of_leading_stock decimal(10,2),
  primary key(biz_date, bankuai_id)
);
alter table dw.bankuai add constraint fk_bankuai_id foreign key(bankuai_id) references dw.dim_bankuai(id);
--alter table dw.bankuai add constraint fk_leading_stock_id foreign key(leading_stock_id) references dw.dim_stock(id);

