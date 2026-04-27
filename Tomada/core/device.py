import os
import asyncio
from tapo import ApiClient

# Classe que representa um dispositivo TAPO
class Device:

    # Construtor
    def __init__(self):
        self.email = os.getenv('TAPO_EMAIL')
        self.password = os.getenv('TAPO_PASSWORD')
        self.ip = os.getenv('TAPO_IP')

        if not self.email or not self.password or not self.ip:
            raise ValueError("Defina TAPO_EMAIL, TAPO_PASSWORD e TAPO_IP.")

        self.plug = None

    # Estabelece a conexão com o dispositivo
    async def connect_plug(self):
        client = ApiClient(self.email, self.password)
        self.plug = await client.p110(self.ip)

    async def ensure_connected(self):
        if self.plug is not None:
            try:
                # Testa a conexão
                await self.plug.get_device_info_json()
                return
            except Exception:
                # Limpa o estado
                self.plug = None

        # Tenta reconectar até 3 vezes
        for _ in range(3):
            try:
                await self.connect_plug()
                return
            except Exception:
                await asyncio.sleep(2)

        raise ConnectionError("Não foi possível conectar ao dispositivo TAPO.")

    async def get_info(self):
        await self.ensure_connected()
        return await self.plug.get_device_info_json()

    async def get_energy(self):
        await self.ensure_connected()
        return await self.plug.get_energy_usage()
    
    async def is_on(self):
        info = await self.get_info()
        return info["device_on"]

    async def turn_on(self):
        await self.ensure_connected()
        await self.plug.on()

    async def turn_off(self):
        await self.ensure_connected()
        await self.plug.off()

# async def main():
#     d = Device()
#     await d.connect_plug()
#     print(await d.is_on())

# asyncio.run(main())
