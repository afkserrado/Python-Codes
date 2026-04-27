import asyncio
import logging
from controller import Controller

logging.basicConfig(
    filename="tapo.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

async def main():
    c = Controller()
    await c.start()

asyncio.run(main())