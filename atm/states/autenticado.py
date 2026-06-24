from atm.states.estado_atm import EstadoATM
from atm.models.resultado_operacion import ResultadoOperacion


class Autenticado(EstadoATM):
    """Sesión activa. El usuario puede operar libremente."""

    def insertar_tarjeta(self, atm) -> ResultadoOperacion:
        return ResultadoOperacion(False, "Ya hay una sesión activa.")

    def ingresar_pin(self, atm, pin: str) -> ResultadoOperacion:
        return ResultadoOperacion(False, "Ya está autenticado/a.")

    def consultar_saldo(self, atm) -> ResultadoOperacion:
        titular = atm.tarjeta.cuenta.titular
        saldo = atm.tarjeta.cuenta.saldo
        return ResultadoOperacion(True, f"{titular} | Saldo disponible: ${saldo:.2f}")

    def depositar(self, atm, monto: float) -> ResultadoOperacion:
        if atm.tarjeta.cuenta.depositar(monto):
            return ResultadoOperacion(True, f"Depósito exitoso de ${monto:.2f}.")
        return ResultadoOperacion(False, "Monto inválido.")

    def extraer(self, atm, monto: float) -> ResultadoOperacion:
        if atm.tarjeta.cuenta.extraer(monto):
            return ResultadoOperacion(True, f"Extracción exitosa de ${monto:.2f}. Retire su dinero.")
        return ResultadoOperacion(False, "Monto inválido o saldo insuficiente.")

    def retirar_tarjeta(self, atm) -> ResultadoOperacion:
        atm.resetear_intentos()
        atm.tarjeta = None
        from atm.states.sin_tarjeta import SinTarjeta
        atm.set_estado(SinTarjeta())
        return ResultadoOperacion(True, "Sesión finalizada. Retire su tarjeta. ¡Hasta luego!")