create table dw.log_stock_transaction(
  row_id integer not null,
  biz_date date not null,
  stock_id varchar(6) not null,
  download_start_time timestamp,
  download_end_time timestamp,
  download_source varchar(32),
  is_download_success varchar(1),
  load_start_time timestamp,
  load_end_time timestamp,
  is_load_success varchar(1),
  primary key(row_id)
);

create sequence dw.seq_log_stock_trans_row_id start with 1;