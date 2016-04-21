create table sched.dim_job(
    id integer not null,
    name varchar(64) not null,
    description varchar(128) not null,
    command varchar(128) not null,
    start_time timestamp,  -- timing trigger job
    condition varchar(1024),  -- SU({job_nm1})&SU({job_nm2}) or FA({job_nm1})
    max_run_time smallint,
    retry smallint,
    primary key(id)
);
create index sched.uidx_job_nm on sched.dim_job(name);
