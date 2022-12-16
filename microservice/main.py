import asyncio
import logger

from fastapi import FastAPI
from router import router

from consumer import PikaClient


#
#
class FooApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.log_incoming_message)

    def log_incoming_message(cls, message: dict):
        logger.info('Here we got incoming message %s', message)


app = FooApp()
app.include_router(router)


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task
