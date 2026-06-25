from models.cuenta import Cuenta


class Tarjeta:
    def __init__(self, numero: int, pin: str, cuenta: Cuenta):
        self.numero = numero
        self._pin = pin
        self.cuenta = cuenta
        self._bloqueada = False # Tarjeta bloqueada?. Atibuto encapsulado.

    def validar_pin(self, pin: str) -> bool:
        return self._pin == pin

    def bloquear(self) -> None:
        """ Bloquea la tarjeta. """
        self._bloqueada = True  # faltaba el _

    def esta_bloqueada(self) -> bool:
        """ Devuelve True si la tarjeta está bloqueada, False en caso contrario. """
        return self._bloqueada