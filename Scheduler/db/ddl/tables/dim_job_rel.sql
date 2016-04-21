create table sched.dim_job_rel(
    id integer not null,
    job_id integer not null,
    downstream_job_id not null,
    trigger_status varchar(2) not null,
    primary key(id)
);
alter table sched.dim_job_rel add constraint fk_dim_job_id foreign key(job_id) references sched.dim_job(id);
alter table sched.dim_job_rel add constraint fk_dim_job_id1 foreign key(downstream_job_id) references sched.dim_job(id);
