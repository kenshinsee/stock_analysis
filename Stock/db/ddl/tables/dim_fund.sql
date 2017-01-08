-- stock table
drop table dw.dim_fund;
create table dw.dim_fund(
  id varchar(6) primary key,
  name varchar(16) not null,
  upd_time timestamp,
  is_valid varchar(1)
);
--Insert into dw.dim_stock values('000000', 'Unknown', now(), 'N');
commit;