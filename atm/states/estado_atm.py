from abc import ABC, abstractmethod
from atm.models.resultado_operacion import ResultadoOperacion


class EstadoATM(ABC):
    """Interfaz base del patrón State.
    
    Ningún estado imprime ni lee input.
    Solo recibe datos, ejecuta lógica y devuelve ResultadoOperacion.
    """

    @abstractmethod
    def insertar_tarjeta(self, atm) -> ResultadoOperacion:
        pass

    @abstractmethod
    def ingresar_pin(self, atm, pin: str) -> ResultadoOperacion:
        pass

    @abstractmethod
    def consultar_saldo(self, atm) -> ResultadoOperacion:
        pass

    @abstractmethod
    def depositar(self, atm, monto: float) -> ResultadoOperacion:
        pass

    @abstractmethod
    def extraer(self, atm, monto: float) -> ResultadoOperacion:
        pass

    @abstractmethod
    def transferir(self, atm, monto: float, destino) -> ResultadoOperacion:
        pass

    @abstractmethod
    def retirar_tarjeta(self, atm) -> ResultadoOperacion:
        pass