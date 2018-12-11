from urllib.parse import urlparse
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from pymongo import MongoClient
from dotenv import load_dotenv
from lib.mortgage_calculator import MortgageCalculator
from flask_socketio import SocketIO
import json
import os
import pika
import kafka_helper
import asyncio
# import websockets

server = Flask(__name__)
server.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(server)

if __name__ == '__main__':
    socketio.run(server)

load_dotenv()

async def consume_events():
    topic = "{}{}".format(os.environ["KAFKA_PREFIX"], os.environ["TOPIC"])
    consumer = kafka_helper.get_kafka_consumer(topic=topic)
    print ("Connected: {}".format(topic))

    for message in consumer:
        print (message)
        await socketio.send(json.dumps(message.value))

asyncio.get_event_loop().run_forever(consume_events())

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
    
