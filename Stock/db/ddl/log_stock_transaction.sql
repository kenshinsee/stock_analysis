create table dw.log_stock_transaction(
  biz_date date not null,
  stock_id varchar(6) not null,
  download_start_time timestamp,
  download_end_time timestamp,
  is_download_success varchar(1),
  load_start_time timestamp,
  load_end_time timestamp,
  is_load_success varchar(1),
  primary key(biz_date, stock_id)
);

