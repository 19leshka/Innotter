import json
import os
from enum import Enum

import pika

from microservice.services import DynamoDBService


class MessageType(Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'

    def __str__(self):
        return self.value


def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST')
    ))
    channel = connection.channel()  # start a channel
    channel.queue_declare(queue=os.getenv('PUBLISH_QUEUE'))

    channel.basic_consume(os.getenv('PUBLISH_QUEUE'),
                          callback,
                          auto_ack=True)

    channel.start_consuming()
    connection.close()


def callback(message):
    with message.process():
        try:
            message = json.loads(message.body.decode())
            message_type = message['type']

            if message_type == MessageType.CREATE.value:
                DynamoDBService.put_item(message)

            elif message_type == MessageType.UPDATE.value:
                DynamoDBService.update_item(message)

            elif message_type == MessageType.DELETE.value:
                DynamoDBService.delete_item(message)

        except Exception as e:
            raise Exception(e)
