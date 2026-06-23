from states.sin_tarjeta import SinTarjeta
from states.tarjeta_insertada import TarjetaInsertada
from states.autenticado import Autenticado
from models.tarjeta import Tarjeta


class ATM:
    def __init__(self):
        # Instancia de cada estado posible
        self.estado_sin_tarjeta = SinTarjeta()
        self.estado_tarjeta_insertada = TarjetaInsertada()
        self.estado_autenticado = Autenticado()

        # Estado inicial
        self._estado_actual = self.estado_sin_tarjeta
        self.tarjeta: Tarjeta | None = None

    def set_estado(self, estado) -> None:
        self._estado_actual = estado

    # --- Acciones del usuario (delegan al estado actual) ---

    def insertar_tarjeta(self, tarjeta: Tarjeta) -> None:
        self.tarjeta = tarjeta
        self._estado_actual.insertar_tarjeta(self)

    def ingresar_pin(self, pin: int) -> None:
        self._estado_actual.ingresar_pin(self, pin)

    def consultar_saldo(self) -> None:
        self._estado_actual.consultar_saldo(self)

    def extraer(self, monto: float) -> None:
        self._estado_actual.extraer(self, monto)

    def depositar(self, monto: float) -> None:
        self._estado_actual.depositar(self, monto)

    def retirar_tarjeta(self) -> None:
        self._estado_actual.retirar_tarjeta(self)
