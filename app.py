from urllib.parse import urlparse
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from pymongo import MongoClient
from dotenv import load_dotenv
from lib.mortgage_calculator import MortgageCalculator
import json
import os
import pika
import kafka_helper
import asyncio
import websockets

server = Flask(__name__)
load_dotenv()

# Parse CLODUAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
                                   credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
channel = connection.channel()  # start a channel
channel.queue_declare(queue=os.environ['QUEUE_NAME'])  # Declare a queue

client = MongoClient(os.environ["MONGODB_URI"])
db = client.get_default_database()

topic = "{}{}".format(os.environ["KAFKA_PREFIX"], os.environ["TOPIC"])
consumer = kafka_helper.get_kafka_consumer(topic=topic)
print ("Connected: {}".format(topic))

async def echo(websocket, path):
    # async for message in websocket:
    for message in consumer:
        print (message)
        await websocket.send(json.dumps(message.value))

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, config['Server']['HOST'], os.environ['PORT']))
asyncio.get_event_loop().run_forever()

@server.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@server.route("/calculate", methods=["POST"])
def consumer():
    data = request.data
    print ("SERVER RECEIVED: {}".format(data))
    
    channel.basic_publish(exchange='', routing_key=os.environ['QUEUE_NAME'], body=data)

    json_data = json.loads(data)
    
    principal = json_data["principal"]
    interest = json_data["interest"]
    years = json_data["years"]
    
    calculator = MortgageCalculator(principal, interest, years)
    payments = calculator.payments()

    return jsonify({ "payments": payments })
    
