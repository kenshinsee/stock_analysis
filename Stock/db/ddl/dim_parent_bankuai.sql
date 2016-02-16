-- parent bankuai table
drop table dw.dim_parent_bankuai;
create table dw.dim_parent_bankuai(
  id serial primary key,
  name varchar(16) not null,
  upd_time timestamp
);
create index uidx_parent_bankuai_nm on dw.dim_parent_bankuai(name);
delete from dw.dim_parent_bankuai;
insert into dw.dim_parent_bankuai(name, upd_time) values('概念板块',now());
insert into dw.dim_parent_bankuai(name, upd_time) values('地域板块',now());
insert into dw.dim_parent_bankuai(name, upd_time) values('行业板块',now());
commit;
