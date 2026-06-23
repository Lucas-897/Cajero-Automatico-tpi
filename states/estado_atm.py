from abc import ABC, abstractmethod


class EstadoATM(ABC):

    @abstractmethod
    def insertar_tarjeta(self, atm) -> None:
        pass

    @abstractmethod
    def ingresar_pin(self, atm, pin: str) -> None:
        pass

    @abstractmethod
    def consultar_saldo(self, atm) -> None:
        pass

    @abstractmethod
    def extraer(self, atm, monto: float) -> None:
        pass

    @abstractmethod
    def depositar(self, atm, monto: float) -> None:
        pass

    @abstractmethod
    def retirar_tarjeta(self, atm) -> None:
        pass
