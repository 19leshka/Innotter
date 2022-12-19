import asyncio

from fastapi import FastAPI
from router import router

from consumer import PikaClient


#
#
class StatisticsApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient()


app = StatisticsApp()
app.include_router(router)


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task
