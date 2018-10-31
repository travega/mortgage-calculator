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

# load_dotenv()

db_parsed = urlparse(os.environ['DATABASE_URL'])
user = db_parsed.username
pwd = db_parsed.password
dbname = db_parsed.path[1:]
host = db_parsed.hostname
port = db_parsed.port
usernames = ['johnb', 'anne_bradshaw', 'georgeH', 'MorrisDashe']
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

        sql = """
            insert into mortgage_calculator.load_enquiries(
                                                            username, 
                                                            principal, 
                                                            interest, 
                                                            years,
                                                            enquiry_source, 
                                                            timestamp
                                                        ) 
            values ('{}', '{}', '{}', '{}', '{}', '{}')
                """.format(random.choice(usernames), principal, interest, years, "Website", timestamp())
        
        cur.execute(sql)
        cur.execute('commit')

        connection.close()

    except Exception as e:
        print("Error occurred: {}".format(e))
        return False 

    return True

def timestamp():
    t = time.time()
    ts = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M%S%f')
    return ts

# set up subscription on the queue
channel.basic_consume(  callback,
                        queue=os.environ['QUEUE_NAME'],
                        no_ack=True)

channel.start_consuming()

connection.close()
