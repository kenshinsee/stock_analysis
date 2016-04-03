create table dw.holiday(
  date varchar(8) not null, --20160101
  iso_date date not null, --2016-01-01
  year integer not null,
  month integer not null,
  day integer not null,
  primary key(date)
);

insert into dw.holiday values
('20160101', '2016-01-01', 2016, 1, 1),
('20160102', '2016-01-02', 2016, 1, 2),
('20160103', '2016-01-03', 2016, 1, 3),
('20160207', '2016-02-07', 2016, 2, 7),
('20160208', '2016-02-08', 2016, 2, 8),
('20160209', '2016-02-09', 2016, 2, 9),
('20160210', '2016-02-10', 2016, 2, 10),
('20160211', '2016-02-11', 2016, 2, 11),
('20160212', '2016-02-12', 2016, 2, 12),
('20160213', '2016-02-13', 2016, 2, 13),
('20160402', '2016-04-02', 2016, 4, 2),
('20160403', '2016-04-03', 2016, 4, 3),
('20160404', '2016-04-04', 2016, 4, 4),
('20160430', '2016-04-30', 2016, 4, 30),
('20160501', '2016-05-01', 2016, 5, 1),
('20160502', '2016-05-02', 2016, 5, 2),
('20160609', '2016-06-09', 2016, 6, 9),
('20160610', '2016-06-10', 2016, 6, 10),
('20160611', '2016-06-11', 2016, 6, 11),
('20160915', '2016-09-15', 2016, 9, 15),
('20160916', '2016-09-16', 2016, 9, 16),
('20160917', '2016-09-17', 2016, 9, 17),
('20161001', '2016-10-01', 2016, 10, 1),
('20161002', '2016-10-02', 2016, 10, 2),
('20161003', '2016-10-03', 2016, 10, 3),
('20161004', '2016-10-04', 2016, 10, 4),
('20161005', '2016-10-05', 2016, 10, 5),
('20161006', '2016-10-06', 2016, 10, 6),
('20161007', '2016-10-07', 2016, 10, 7);
commit;