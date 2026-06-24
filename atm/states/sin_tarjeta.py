from atm.states.estado_atm import EstadoATM
from atm.models.resultado_operacion import ResultadoOperacion


class SinTarjeta(EstadoATM):
    """El ATM está libre. Solo acepta insertar tarjeta."""

    def insertar_tarjeta(self, atm) -> ResultadoOperacion:
        from atm.states.tarjeta_insertada import TarjetaInsertada
        atm.set_estado(TarjetaInsertada())
        return ResultadoOperacion(True, "Tarjeta insertada. Ingrese su PIN.")

    def ingresar_pin(self, atm, pin: str) -> ResultadoOperacion:
        return ResultadoOperacion(False, "Primero debe insertar una tarjeta.")

    def consultar_saldo(self, atm) -> ResultadoOperacion:
        return ResultadoOperacion(False, "Primero debe insertar una tarjeta.")

    def depositar(self, atm, monto: float) -> ResultadoOperacion:
        return ResultadoOperacion(False, "Primero debe insertar una tarjeta.")

    def extraer(self, atm, monto: float) -> ResultadoOperacion:
        return ResultadoOperacion(False, "Primero debe insertar una tarjeta.")

    def retirar_tarjeta(self, atm) -> ResultadoOperacion:
        return ResultadoOperacion(False, "No hay ninguna tarjeta insertada.")