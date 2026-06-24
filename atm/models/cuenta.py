from atm.models.transaccion import Transaccion, TipoTransaccion


class Cuenta:
    """Representa una cuenta bancaria simplificada.
    
    El saldo nunca se modifica directamente: siempre pasa por depositar() o extraer(),
    que registran la transacción y recalculan el saldo automáticamente.
    """

    _contador = 0  # Compartido entre todas las instancias para generar nros únicos

    def __init__(self, titular: str, saldo_inicial: float = 0.0):
        """
        Args:
            titular: Nombre del dueño de la cuenta.
            saldo_inicial: Saldo de arranque. Si es negativo se trata como 0.
        """
        Cuenta._contador += 1
        self._nro_cuenta = Cuenta._contador
        self._titular = titular
        self._dni: str | None = None
        self._saldo_inicial = max(0.0, float(saldo_inicial))
        self._saldo = float(self._saldo_inicial)
        self._transacciones: list[Transaccion] = []

    # ── Properties ────────────────────────────────────────────────

    @property
    def nro_cuenta(self) -> int:
        """Número de cuenta único. Se asigna automáticamente al crear la cuenta."""
        return self._nro_cuenta

    @property
    def titular(self) -> str:
        """Nombre del titular. Solo lectura."""
        return self._titular

    @property
    def saldo(self) -> float:
        """Saldo actual de la cuenta. Solo lectura.
        Para modificarlo usá depositar() o extraer()."""
        return self._saldo

    @property
    def dni(self) -> str | None:
        """DNI del titular. Puede ser None si no fue asignado todavía."""
        return self._dni

    @dni.setter
    def dni(self, value: str) -> None:
        """Asigna el DNI después de validarlo. Solo acepta strings no vacíos."""
        if value is None:
            self._dni = None
            return
        if not isinstance(value, str) or not value.strip():
            raise ValueError("DNI inválido")
        self._dni = value.strip()

    # ── Consultas ─────────────────────────────────────────────────

    def get_transacciones(self) -> list[Transaccion]:
        """Devuelve una copia del historial de transacciones.
        
        Es una copia para que nadie pueda modificar el historial interno
        desde afuera de la clase.
        """
        return list(self._transacciones)

    # ── Operaciones ───────────────────────────────────────────────

    def depositar(self, monto: float) -> bool:
        """Deposita dinero en la cuenta.

        Args:
            monto: Cantidad a depositar. Debe ser mayor a cero.

        Returns:
            True si el depósito fue exitoso, False si el monto es inválido.
        """
        if monto <= 0:
            print("[ERROR] El monto debe ser mayor a cero.")
            return False
        self._registrar_transaccion(TipoTransaccion.DEPOSITO, monto)
        return True

    def extraer(self, monto: float) -> bool:
        """Extrae dinero de la cuenta si hay saldo suficiente.

        Args:
            monto: Cantidad a extraer. Debe ser mayor a cero y no superar el saldo.

        Returns:
            True si la extracción fue exitosa, False si el monto es inválido o no hay saldo.
        """
        if monto <= 0:
            print("[ERROR] El monto debe ser mayor a cero.")
            return False
        if monto > self._saldo:
            print("[ERROR] Saldo insuficiente.")
            return False
        self._registrar_transaccion(TipoTransaccion.EXTRACCION, monto)
        return True

    def transferir(self, monto: float, destino: "Cuenta") -> bool:
        """Transfiere un monto a otra cuenta.
        
        Args:
            monto: Cantidad a transferir. Debe ser mayor a cero y no superar el saldo.
            destino: Cuenta que recibe el dinero.

        Returns:
            True si la transferencia fue exitosa, False en caso contrario.
        """
        if monto <= 0:
            print("[ERROR] El monto debe ser mayor a cero.")
            return False
        if monto > self._saldo:
            print("[ERROR] Saldo insuficiente.")
            return False

        self._registrar_transaccion(TipoTransaccion.TRANSFERENCIA, monto)
        destino.depositar(monto)
        return True

    # ── Internos ──────────────────────────────────────────────────

    def _registrar_transaccion(self, tipo: TipoTransaccion, monto: float) -> None:
        """Crea y guarda la transacción, luego actualiza el saldo.
        
        Es privado porque nadie de afuera debería registrar transacciones
        directamente — siempre tienen que pasar por depositar() o extraer().
        """
        self._transacciones.append(Transaccion(tipo, monto))
        self._actualizar_saldo()

    def _actualizar_saldo(self) -> None:
        """Recalcula el saldo sumando y restando todas las transacciones desde el saldo inicial.
        
        Recalcular desde cero cada vez (en lugar de sumar/restar incremental)
        evita que errores se acumulen si el historial se modifica o se carga desde afuera.
        """
        saldo = float(self._saldo_inicial)
        for t in self._transacciones:
            if t.tipo == TipoTransaccion.DEPOSITO:
                saldo += t.monto
            else:
                saldo -= t.monto
        self._saldo = max(0.0, saldo)