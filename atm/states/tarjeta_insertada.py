from atm.states.estado_atm import EstadoATM
from atm.models.resultado_operacion import ResultadoOperacion


class TarjetaInsertada(EstadoATM):
    """Tarjeta insertada, sesión sin autenticar. Solo acepta PIN o retirar tarjeta."""

    def insertar_tarjeta(self, atm) -> ResultadoOperacion:
        return ResultadoOperacion(False, "Ya hay una tarjeta insertada.")

    def ingresar_pin(self, atm, pin: str) -> ResultadoOperacion:
        if atm.tarjeta.bloqueada:
            return ResultadoOperacion(False, "Tarjeta bloqueada. Comuníquese con su banco.")

        if atm.tarjeta.validar_pin(pin):
            atm.resetear_intentos()
            from atm.states.autenticado import Autenticado
            atm.set_estado(Autenticado())
            return ResultadoOperacion(True, "PIN correcto. Bienvenido/a.")

        bloqueada = atm.registrar_intento_fallido()
        if bloqueada:
            atm.tarjeta = None
            from atm.states.sin_tarjeta import SinTarjeta
            atm.set_estado(SinTarjeta())
            return ResultadoOperacion(False, "Demasiados intentos. Tarjeta bloqueada y retenida.")

        restantes = atm.MAX_INTENTOS_PIN - atm._intentos_pin
        return ResultadoOperacion(False, f"PIN incorrecto. Intentos restantes: {restantes}.")

    def consultar_saldo(self, atm) -> ResultadoOperacion:
        return ResultadoOperacion(False, "Primero debe ingresar su PIN.")

    def depositar(self, atm, monto: float) -> ResultadoOperacion:
        return ResultadoOperacion(False, "Primero debe ingresar su PIN.")

    def extraer(self, atm, monto: float) -> ResultadoOperacion:
        return ResultadoOperacion(False, "Primero debe ingresar su PIN.")

    def retirar_tarjeta(self, atm) -> ResultadoOperacion:
        atm.resetear_intentos()
        atm.tarjeta = None
        from atm.states.sin_tarjeta import SinTarjeta
        atm.set_estado(SinTarjeta())
        return ResultadoOperacion(True, "Tarjeta retirada.")