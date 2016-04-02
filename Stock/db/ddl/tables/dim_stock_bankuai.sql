-- bridge table for stock and bankuai
drop table dw.dim_stock_bankuai;
create table dw.dim_stock_bankuai(
  stock_id varchar(6) not null,
  bankuai_id integer not null,
  upd_time timestamp,
  is_valid varchar(1), --Y/N
  primary key(stock_id,bankuai_id)
);
alter table dw.dim_stock_bankuai add constraint fk_stock_id foreign key(stock_id) references dw.dim_stock(id);
alter table dw.dim_stock_bankuai add constraint fk_bankuai_id foreign key(bankuai_id) references dw.dim_bankuai(id);
create index idx_stock_id on dw.dim_stock_bankuai(stock_id);
create index idx_bankuai_id on dw.dim_stock_bankuai(bankuai_id);
