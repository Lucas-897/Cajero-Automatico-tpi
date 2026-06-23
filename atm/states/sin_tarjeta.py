from atm.states.estado_atm import EstadoATM


class SinTarjeta(EstadoATM):

    def insertar_tarjeta(self, atm) -> None:
        print("[ATM] Tarjeta insertada. Por favor ingrese su PIN.")
        atm.set_estado(atm.estado_tarjeta_insertada)

    def ingresar_pin(self, atm, pin: str) -> None:
        print("[ATM] Primero debe insertar una tarjeta.")

    def consultar_saldo(self, atm) -> None:
        print("[ATM] Primero debe insertar una tarjeta.")

    def extraer(self, atm, monto: float) -> None:
        print("[ATM] Primero debe insertar una tarjeta.")

    def depositar(self, atm, monto: float) -> None:
        print("[ATM] Primero debe insertar una tarjeta.")

    def retirar_tarjeta(self, atm) -> None:
        print("[ATM] No hay ninguna tarjeta insertada.")
