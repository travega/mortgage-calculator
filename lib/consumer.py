from urllib.parse import urlparse
from pymongo import MongoClient
from dotenv import load_dotenv
import psycopg2
import time
import datetime
import random
import json
import pika
import os

load_dotenv()

db_parsed = urlparse(os.environ['DATABASE_URL'])
user = db_parsed.username
pwd = db_parsed.password
dbname = db_parsed.path[1:]
host = db_parsed.hostname
port = db_parsed.port
usernames = ['John McAnn', 'Rachel Sand', 'Ivan Green', 'Morris Dashe']
client = MongoClient(os.environ["MONGODB_URI"])
db = client.get_default_database()

url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
                                   credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params)
channel = connection.channel()

def callback(ch, method, properties, body):
    print ("CONSUMER RECEIVED: {}".format(body))
    doc = json.loads(body)
    to_mongo(doc)
    to_pg(doc)

def to_mongo(mongo_doc):
    sensor_data = db['load_enquiries']
    sensor_data.insert_one(mongo_doc)

def to_pg(payload):
    try:
        connection = psycopg2.connect(dbname=dbname, host=host, port=port, user=user, password=pwd)
        cur = connection.cursor()

        principal = payload['principal']
        interest = payload['interest']
        years = payload['years']
        name = random.choice(usernames)
        first_name = name.split(' ')[0]
        last_name = name.split(' ')[1]
        email = "{}.{}@example.com".format(first_name, last_name)

        sql = """
            insert into salesforce.Lead(
                                                            firstname,
                                                            lastname,
                                                            name,
                                                            email,
                                                            company,
                                                            principal__c, 
                                                            interest_rate__c, 
                                                            term_years__c,
                                                            leadsource, 
                                                            createddate,
                                                            external_id__c
                                                        ) 
            values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                """.format(first_name,last_name, name, email, 'n/a', principal, interest, years, "Website", timestamp('%d/%m/%Y'), timestamp('%Y%m%d%H%M%S%f'))
        
        cur.execute(sql)
        cur.execute('commit')

        connection.close()

    except Exception as e:
        print("Error occurred: {}".format(e))
        return False 

    return True

def timestamp(format):
    t = time.time()
    val = datetime.datetime.fromtimestamp(t).strftime(format)
    return val

# set up subscription on the queue
channel.basic_consume(  callback,
                        queue=os.environ['QUEUE_NAME'],
                        no_ack=True)

channel.start_consuming()

connection.close()
