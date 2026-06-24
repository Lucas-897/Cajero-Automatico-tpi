from atm.models import Cuenta, Tarjeta, ResultadoOperacion
from atm.states import SinTarjeta, EstadoATM


class ATM:
    """Máquina expendedora de efectivo. Implementa el patrón State.
    
    Toda acción del usuario se delega al estado actual, que decide
    si la operación es válida y cuál es el próximo estado.
    
    Estados posibles:
        SinTarjeta -> TarjetaInsertada -> Autenticado -> SinTarjeta
    """

    MAX_INTENTOS_PIN = 3

    def __init__(self):
        self._estado_actual = SinTarjeta()
        self.tarjeta: Tarjeta | None = None
        self._intentos_pin: int = 0

    # ── Estado ────────────────────────────────────────────────────

    def set_estado(self, estado: EstadoATM) -> None:
        """Cambia el estado actual. Lo llaman los estados internamente."""
        self._estado_actual = estado

    # ── Sesión ────────────────────────────────────────────────────

    def registrar_intento_fallido(self) -> bool:
        """Registra un intento fallido de PIN.
        
        Returns:
            True si la tarjeta fue bloqueada (se agotaron los intentos).
            False si todavía quedan intentos.
        """
        self._intentos_pin += 1
        if self._intentos_pin >= self.MAX_INTENTOS_PIN:
            if self.tarjeta:
                self.tarjeta.bloquear()
            return True
        return False

    def resetear_intentos(self) -> None:
        """Resetea el contador de intentos. Se llama al autenticarse correctamente."""
        self._intentos_pin = 0

    # ── Acciones del usuario (delegan al estado actual) ───────────

    def insertar_tarjeta(self, tarjeta: Tarjeta) -> ResultadoOperacion:
        self.tarjeta = tarjeta
        return self._estado_actual.insertar_tarjeta(self)

    def ingresar_pin(self, pin: str) -> ResultadoOperacion:
        return self._estado_actual.ingresar_pin(self, pin)

    def consultar_saldo(self) -> ResultadoOperacion:
        return self._estado_actual.consultar_saldo(self)

    def depositar(self, monto: float) -> ResultadoOperacion:
        return self._estado_actual.depositar(self, monto)

    def extraer(self, monto: float) -> ResultadoOperacion:
        return self._estado_actual.extraer(self, monto)

    def retirar_tarjeta(self) -> ResultadoOperacion:
        return self._estado_actual.retirar_tarjeta(self)