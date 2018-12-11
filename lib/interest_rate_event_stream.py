from flask import Flask
# from flask import render_template
import os
import kafka_helper
import json
import asyncio
import websockets

topic = "{}{}".format(os.environ["KAFKA_PREFIX"], os.environ["TOPIC"])
consumer = kafka_helper.get_kafka_consumer(topic=topic)
print ("Connected: {}".format(topic))

async def echo(websocket, path):
    # async for message in websocket:
    for message in consumer:
        print (message)
        await websocket.send(json.dumps(message.value))

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, '0.0.0.0', os.environ['PORT']))
asyncio.get_event_loop().run_forever()
