import asyncio
from controller import Controller

async def main():
    c = Controller()
    await c.start()

asyncio.run(main())