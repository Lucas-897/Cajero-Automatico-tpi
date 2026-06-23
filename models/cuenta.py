from models.transaccion import Transaccion


class Cuenta:
    def __init__(self, titular: str, saldo: float):
        self.titular = titular
        self.saldo = saldo
        self.transacciones: list[Transaccion] = []

    def consultar_saldo(self) -> float:
        return self.saldo

    def extraer(self, monto: float) -> bool:
        if monto <= 0:
            print("[ERROR] El monto debe ser mayor a cero.")
            return False
        if monto > self.saldo:
            print("[ERROR] Saldo insuficiente.")
            return False
        self.saldo -= monto
        self.transacciones.append(Transaccion("EXTRACCION", monto))
        return True

    def depositar(self, monto: float) -> bool:
        if monto <= 0:
            print("[ERROR] El monto debe ser mayor a cero.")
            return False
        self.saldo += monto
        self.transacciones.append(Transaccion("DEPOSITO", monto))
        return True
