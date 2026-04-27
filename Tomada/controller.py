import asyncio
import logging
from core.device import Device
from logic.battery import Battery

class Controller:

    def __init__(self):
        self.device = Device()
        self.battery = Battery()

    async def start(self):
        while True:
            try:
                info = self.battery.get_battery_info()
                percent = info["Percentual"]
                charging = info["Carregando"]
                is_on = await self.device.is_on()

                logging.info(f"Bateria: {percent}% | Carregando: {charging}")

                # Liga a tomada
                if percent <= 20 and not is_on:
                    logging.info("Ligando a tomada...")
                    await self.device.turn_on()

                # Desliga a tomada
                elif percent >= 80 and is_on:
                    logging.info("Desligando a tomada...")
                    await self.device.turn_off()

                # Intervalo de verificação a cada 1 minuto
                await asyncio.sleep(60) 

            except Exception as e:
                logging.error(f"Erro no loop: {e}")
                self.device.plug = None # Força a reconexão
                await asyncio.sleep(10)