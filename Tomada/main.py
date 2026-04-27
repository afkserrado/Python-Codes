import asyncio
import logging
import os
from controller import Controller

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    filename=os.path.join(BASE_DIR, "tapo.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    force=True
)

async def main():
    c = Controller()
    await c.start()

asyncio.run(main())