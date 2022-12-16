import json
import os

import pika


def producer(data):
    params = pika.URLParameters(os.getenv('AMQP_URL'))
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=os.getenv('PUBLISH_QUEUE'))
    channel.basic_publish(
        exchange='',
        routing_key=os.getenv('PUBLISH_QUEUE'),
        body=json.dumps(data)
    )
