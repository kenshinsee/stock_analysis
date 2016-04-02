-- daily stock data
create table dw.stock(
  biz_date date not null,
  stock_id varchar(6) not null,
  open_price decimal(12,4),
  top_price decimal(12,4),
  floor_price decimal(12,4),
  close_price decimal(12,4),
  adj_close_price decimal(12,4),
  yesterday_close_price decimal(12,4), 
  volume decimal(22,2), --round-lot
  amount decimal(22,2), --10 thousands
  outer_disc decimal(22,2), --round-lot
  inner_disc decimal(22,2), --round-lot
  rise_price decimal(12,4),
  rise decimal(12,4), --%
  turnover_ratio decimal(12,4),
  PE_ratio decimal(12,4),
  amplitudes decimal(12,4), --%
  circulation_market_value decimal(12,2), -- 100 million
  total_market_value decimal(12,2), -- 100 million
  PB_ratio decimal(12,4),
  high_limit decimal(12,4),
  low_limit decimal(12,4),
  source varchar(16),
  primary key(biz_date, stock_id)
);
alter table dw.stock add constraint fk_stock_id foreign key(stock_id) references dw.dim_stock(id);

