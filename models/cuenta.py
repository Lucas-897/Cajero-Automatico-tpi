from models.transaccion import Transaccion


class Cuenta:
    def __init__(self, titular: str, saldo: float):
        self._titular = titular
        self._saldo = saldo
        self._transacciones: list[Transaccion] = []

    # usamos @property para poder leer el saldo como un atributo, pero no permitir modificarlo directamente
    @property
    def titular(self) -> str:
        return self._titular
    
    @property
    def saldo(self) -> float:
        return self._saldo
    @property
    def transacciones(self) -> list[Transaccion]:
        return self._transacciones
    
    def consultar_saldo(self) -> float:
        return self._saldo

    def extraer(self, monto: float) -> bool:
        if monto <= 0:
            print("[ERROR] El monto debe ser mayor a cero.")
            return False
        if monto > self._saldo:
            print("[ERROR] Saldo insuficiente.")
            return False
        self._saldo -= monto
        self._transacciones.append(Transaccion("EXTRACCION", monto))
        return True

    def depositar(self, monto: float) -> bool:
        if monto <= 0:
            print("[ERROR] El monto debe ser mayor a cero.")
            return False
        self._saldo += monto
        self._transacciones.append(Transaccion("DEPOSITO", monto))
        return True
