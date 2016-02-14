----------------------------
-- create user in shell
----------------------------
createuser -P -d -U postgres stock;
createuser -P -d -U postgres hong;

----------------------------
-- create tablespace and database in psql
----------------------------
create tablespace "StockDbs1" owner stock location '/app/database/postgres/pg_tbs/stock_dbs'
create database "StockDb" owner stock encoding 'UTF8' tablespace "StockDbs1";
grant all privileges on database "StockDb" to stock;
grant all privileges on database "StockDb" to hong;

----------------------------
-- authorization
----------------------------
If a linux user is also a database user (has same name), it can just connect to a database via "psql -d $database"
If a linux user is not a databbase user, it needs to specify the database user name within the psql command, like the example below

-- connect to database with a db user
psql stock -h 127.0.0.1 -d StockDb

--------------------------------------------------------------------------------------------------------------------------------------------
-- initialize database structure
--------------------------------------------------------------------------------------------------------------------------------------------
create schema dw;

-- parent bankuai table
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

-- bankuai table
create table dw.dim_bankuai(
  id serial primary key,
  name varchar(16) not null,
  parent_bankuai_id integer not null,
  upd_time timestamp,
  is_valid varchar(1) --Y/N
);
create index uidx_bankuai_nm on dw.dim_bankuai(name);
alter table dw.dim_bankuai add constraint fk_parent_bankuai_id foreign key(parent_bankuai_id) references dw.dim_parent_bankuai(id);

-- stock table
create table dw.dim_stock(
  id varchar(6) primary key,
  name varchar(16) not null,
  upd_time timestamp,
  is_valid varchar(1)
);

-- bridge table for stock and bankuai
create table dw.dim_stock_bankuai(
  stock_id varchar(6) not null,
  bankuai_id integer not null,
  upd_time timestamp,
  is_valid varchar(1) --Y/N
);
alter table dw.dim_stock_bankuai add constraint fk_stock_id foreign key(stock_id) references dw.dim_stock(id);
alter table dw.dim_stock_bankuai add constraint fk_bankuai_id foreign key(bankuai_id) references dw.dim_bankuai(id);
create index idx_stock_id on dw.dim_stock_bankuai(stock_id);
create index idx_bankuai_id on dw.dim_stock_bankuai(bankuai_id);

-- daily bankuai data
create table dw.bankuai(
  id serial primary key,
  biz_date date not null,
  bankuai_id integer not null,
  rise decimal(10,2),
  market_value_in_million decimal(12,2),
  turnover_rate decimal(5,2),
  num_of_rise integer,
  num_of_drop integer,
  leading_stock_id varchar(6),
  rise_of_leading_stock decimal(10,2)
);
create index uidx_bankuai_dt_id on dw.bankuai(biz_date, bankuai_id);
alter table dw.bankuai add constraint fk_bankuai_id foreign key(bankuai_id) references dw.dim_bankuai(id);
alter table dw.bankuai add constraint fk_leading_stock_id foreign key(leading_stock_id) references dw.dim_stock(id);


