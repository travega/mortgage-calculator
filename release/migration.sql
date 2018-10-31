create schema if not exists mortgage_calculator;

create sequence if not exists serial;

create table if not exists mortgage_calculator.load_enquiries (
  id integer default nextval('serial') not null
    constraint load_enquiries_pkey
    primary key,
  username          varchar(100),
  principal         decimal,
  interest          decimal,
  years             numeric,
  enquiry_source    numeric,
  timestamp         varchar(100),
  created_at        timestamp default now()
);