-- job
create table dw.job(
  row_id integer not null,
  name varchar(128) not null,
  start_time timestamp,
  end_time timestamp,
  is_success varchar(1)
);

create sequence dw.seq_job_row_id start with 1;