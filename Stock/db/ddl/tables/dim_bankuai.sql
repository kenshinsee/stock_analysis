drop table dw.dim_bankuai;
create table dw.dim_bankuai(
  id serial primary key,
  name varchar(16) not null,
  parent_bankuai_id integer not null,
  upd_time timestamp,
  is_valid varchar(1) --Y/N
);
create index dw.uidx_bankuai_nm on dw.dim_bankuai(name);
alter table dw.dim_bankuai add constraint fk_parent_bankuai_id foreign key(parent_bankuai_id) references dw.dim_parent_bankuai(id);
