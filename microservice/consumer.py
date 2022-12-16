import json, os, logger, pika

from aio_pika import connect_robust


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
            try:
                message = json.loads(message.body.decode())
                # message_type = message['type']
                #
                # if message_type == MessageType.CREATE.value:
                #     AWSManager.put_item(message)
                #
                # elif message_type == MessageType.UPDATE.value:
                #     AWSManager.update_item(message)
                #
                # elif message_type == MessageType.DELETE.value:
                #     AWSManager.delete_item(message)

            except Exception as e:
                logger.error(e)
