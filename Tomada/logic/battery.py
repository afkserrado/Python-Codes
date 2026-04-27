import psutil

# Classe que representa a bateria do notebook
class Battery:

    # Lê a bateria
    def _read(self):
        battery = psutil.sensors_battery()

        if battery is None:
            raise ValueError("Notebook sem bateria.")

        return battery

    # Retorna o percentual de carga
    def get_percent(self):
        battery = self._read()
        return int(battery.percent)

    # Retorna 'True' se estiver carregando; 'False' caso contrário
    def get_status(self):
        battery = self._read()
        return battery.power_plugged

    def get_battery_info(self):
        return {
            "Percentual": self.get_percent(),
            "Carregando": self.get_status(),
        }
