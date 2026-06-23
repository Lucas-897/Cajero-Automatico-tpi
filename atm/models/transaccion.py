from datetime import datetime


class Transaccion:
    def __init__(self, tipo: str, monto: float):
        self.tipo = tipo
        self.monto = monto
        self.fecha = datetime.now()

    def __str__(self):
        fecha_str = self.fecha.strftime("%d/%m/%Y %H:%M:%S")
        return f"[{fecha_str}] {self.tipo}: ${self.monto:.2f}"
