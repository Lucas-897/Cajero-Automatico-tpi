from models import Tarjeta
from states import SinTarjeta, TarjetaInsertada, Autenticado


class ATM:

    _MAX_INTENTOS_PIN = 3

    def __init__(self):
        # Instancia de cada estado posible
        self.estado_sin_tarjeta = SinTarjeta()
        self.estado_tarjeta_insertada = TarjetaInsertada()
        self.estado_autenticado = Autenticado()
        self._intentos_pin = self._MAX_INTENTOS_PIN

        # Estado inicial
        self._estado_actual = self.estado_sin_tarjeta
        self.tarjeta: Tarjeta | None = None

    def set_estado(self, estado) -> None:
        self._estado_actual = estado

    # --- Acciones del usuario (delegan al estado actual) ---

    def insertar_tarjeta(self, tarjeta: Tarjeta) -> None:
        self.tarjeta = tarjeta
        self._estado_actual.insertar_tarjeta(self)

    def ingresar_pin(self, pin: str) -> None:
        self._estado_actual.ingresar_pin(self, pin)

    def consultar_saldo(self) -> None:
        self._estado_actual.consultar_saldo(self)

    def extraer(self, monto: float) -> None:
        self._estado_actual.extraer(self, monto)

    def depositar(self, monto: float) -> None:
        self._estado_actual.depositar(self, monto)

    def retirar_tarjeta(self) -> None:
        self._estado_actual.retirar_tarjeta(self)

    
    # ------------- INTENTOS DE INGRESO DE PIN ------------------------
    def registrar_intento_fallido(self) -> bool:
        """ Registra un intento fallido de ingreso de PIN y devuelve True si se agotaron los intentos. """
        self._intentos_pin -= 1
        return self._intentos_pin <= 0 # ¿se agotaron los intentos?


    def intentos_restantes(self) -> int:
        """ Devuelve la cantidad de intentos de PIN restantes antes de bloquear la tarjeta. """
        return self._intentos_pin
    
    def resetear_intentos(self) -> None:
        """ Resetea el contador de intentos de PIN a su valor máximo. """
        self._intentos_pin = self._MAX_INTENTOS_PIN
