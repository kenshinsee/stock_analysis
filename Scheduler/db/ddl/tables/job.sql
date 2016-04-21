create table sched.job(
    row_id integer not null,
    job_id integer not null,
    start_time timestamp,
    end_time timestamp,
    status varchar(2), -- SU|FA|IC
    primary key(row_id)
);
alter table sched.job add constraint fk_dim_job_id foreign key(job_id) references sched.dim_job(id);
