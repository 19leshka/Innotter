import json
import os

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.getenv('RABBITMQ_HOST')
))
channel = connection.channel()
channel.queue_declare(queue=os.getenv('PUBLISH_QUEUE'))

# channel.exchange_declare(
#     exchange='page'
# )


def publish(message: dict) -> None:
    channel.basic_publish(
        exchange='',
        routing_key=os.getenv('PUBLISH_QUEUE'),
        body=json.dumps(message)
    )