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

server = Flask(__name__)
load_dotenv()

# Parse CLODUAMQP_URL (fallback to localhost)
client = MongoClient(os.environ["MONGODB_URI"])
db = client.get_default_database()
channel = None


def init():
    global channel
    url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
    url = urlparse(url_str)
    params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
                                       credentials=pika.PlainCredentials(url.username, url.password))

    connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
    channel = connection.channel()  # start a channel
    channel.queue_declare(queue=os.environ['QUEUE_NAME'])  # Declare a queue


init()


@server.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@server.route("/calculate", methods=["POST"])
def consumer():
    data = request.data
    print ("SERVER RECEIVED: {}".format(data))

    try:
        publish(data)
    except Exception:
        init()
        publish(data)

    json_data = json.loads(data)

    principal = json_data["principal"].replace(",", "")
    interest = json_data["interest"]
    years = json_data["years"]

    calculator = MortgageCalculator(principal, interest, years)
    payments = calculator.payments()

    return jsonify({"payments": payments})


def publish(data):
    channel.basic_publish(
        exchange='', routing_key=os.environ['QUEUE_NAME'], body=data)
