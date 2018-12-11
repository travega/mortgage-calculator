from flask import Flask
# from flask import render_template
import os
import kafka_helper
import json
import asyncio

topic = "{}{}".format(os.environ["KAFKA_PREFIX"], os.environ["TOPIC"])
consumer = kafka_helper.get_kafka_consumer(topic=topic)
print ("Connected: {}".format(topic))

async def echo():
    # async for message in websocket:
    for message in consumer:
        await print (message)
        # await websocket.send(json.dumps(message.value))

asyncio.get_event_loop().run_until_complete(echo())
asyncio.get_event_loop().run_forever()
