from models.cuenta import Cuenta


class Tarjeta:
    def __init__(self, numero: int, pin: str, cuenta: Cuenta):
        self.numero = numero
        self._pin = pin
        self.cuenta = cuenta

    def validar_pin(self, pin: str) -> bool:
        return self._pin == pin
