import json
import os
import logger

import pika
from aio_pika import connect_robust

from services import DynamoDBService


class PikaClient:
    def __init__(self, process_callable):
        params = pika.URLParameters(os.getenv('AMQP_URL'))
        self.publish_queue_name = os.getenv('PUBLISH_QUEUE')
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable

    async def consume(self, loop):
        connection = await connect_robust(os.getenv('AMQP_URL'), loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue(os.getenv('CONSUME_QUEUE'))
        await queue.consume(self.process_incoming_message, no_ack=False)
        return connection

    async def process_incoming_message(self, message):
        async with message.process():
            message = json.loads(message.body.decode())
            message_type = message['type']

            if message_type == "create":
                DynamoDBService.put_item(message)
            elif message_type == "delete":
                DynamoDBService.delete_item(message)
            elif message_type == "add_like":
                DynamoDBService.add_like(message)
            elif message_type == "del_like":
                DynamoDBService.delete_like(message)
            elif message_type == "add_post":
                DynamoDBService.add_post(message)
            elif message_type == "del_post":
                DynamoDBService.delete_post(message)
            elif message_type == "add_follower":
                DynamoDBService.add_follower(message)
            elif message_type == "del_follower":
                DynamoDBService.del_follower(message)
