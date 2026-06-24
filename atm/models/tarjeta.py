from atm.models.cuenta import Cuenta


class Tarjeta:
    """Capa de seguridad y acceso a una cuenta bancaria.
    
    Controla quién puede operar sobre la cuenta mediante PIN y bloqueo.
    No maneja dinero directamente — eso es responsabilidad de Cuenta.
    """

    def __init__(self, numero: int, pin: str, cuenta: Cuenta):
        """
        Args:
            numero: Número identificador de la tarjeta.
            pin: PIN inicial de 4 dígitos.
            cuenta: Cuenta bancaria asociada a esta tarjeta.
        """
        self._numero = numero
        self._pin = pin
        self._cuenta = cuenta
        self._bloqueada = False

    # ── Properties ────────────────────────────────────────────────

    @property
    def numero(self) -> int:
        """Número de la tarjeta. Solo lectura."""
        return self._numero

    @property
    def cuenta(self) -> Cuenta:
        """Cuenta bancaria asociada. Solo lectura."""
        return self._cuenta

    @property
    def bloqueada(self) -> bool:
        """True si la tarjeta está bloqueada y no puede usarse."""
        return self._bloqueada

    # ── PIN ───────────────────────────────────────────────────────

    def validar_pin(self, pin: str) -> bool:
        """Verifica si el PIN ingresado es correcto.
        
        No registra intentos fallidos — esa responsabilidad es del ATM,
        que llama a bloquear() cuando corresponde.

        Returns:
            True si el PIN es correcto, False si no lo es.
        """
        return self._pin == pin

    def cambiar_pin(self, nuevo_pin: str) -> bool:
        """Cambia el PIN de la tarjeta.
        
        Args:
            nuevo_pin: Nuevo PIN. Debe tener exactamente 4 dígitos numéricos.

        Returns:
            True si el cambio fue exitoso, False si el formato es inválido.
        """
        if len(nuevo_pin) != 4 or not nuevo_pin.isdigit():
            print("[ERROR] El PIN debe tener exactamente 4 dígitos numéricos.")
            return False
        self._pin = nuevo_pin
        return True

    # ── Bloqueo ───────────────────────────────────────────────────

    def bloquear(self) -> None:
        """Bloquea la tarjeta permanentemente.
        
        Una vez bloqueada, el ATM debe rechazar cualquier operación.
        Se llama desde el ATM después de N intentos fallidos de PIN.
        """
        self._bloqueada = True

    # ── Representación ────────────────────────────────────────────

    def __str__(self):
        estado = "BLOQUEADA" if self._bloqueada else "activa"
        return f"Tarjeta {self._numero} [{estado}] - Titular: {self._cuenta.titular} - Saldo: ${self._cuenta.saldo:.2f}"