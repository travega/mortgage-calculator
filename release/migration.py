from urllib.parse import urlparse
import psycopg2
import os

db_parsed = urlparse(os.environ['DATABASE_URL'])
user = db_parsed.username
pwd = db_parsed.password
dbname = db_parsed.path[1:]
host = db_parsed.hostname
port = db_parsed.port
queue_name = os.environ['QUEUE_NAME']

connection = psycopg2.connect(
    dbname=dbname, host=host, port=port, user=user, password=pwd)
cur = connection.cursor()

query = """create schema if not exists mortgage_calculator;

create sequence if not exists serial;

create table if not exists mortgage_calculator.{0} (
  id integer default nextval('serial') not null
    constraint {0}_pkey
    primary key,
    username          varchar(100),
    principal         decimal,
    interest          decimal,
    years             numeric,
    enquiry_source    varchar(100),
    timestamp         varchar(100),
    created_at        timestamp default now()
);""".format(queue_name)

cur.execute(query)
cur.execute("commit")
connection.close()
