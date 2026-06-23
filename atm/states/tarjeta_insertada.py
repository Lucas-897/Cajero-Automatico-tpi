from atm.states.estado_atm import EstadoATM

MAX_INTENTOS = 3


class TarjetaInsertada(EstadoATM):

    def __init__(self):
        self.intentos = 0

    def insertar_tarjeta(self, atm) -> None:
        print("[ATM] Ya hay una tarjeta insertada.")

    def ingresar_pin(self, atm, pin: str) -> None:
        if atm.tarjeta.validar_pin(pin):
            self.intentos = 0
            print("[ATM] PIN correcto. Bienvenido/a.")
            atm.set_estado(atm.estado_autenticado)
        else:
            self.intentos += 1
            restantes = MAX_INTENTOS - self.intentos
            if restantes > 0:
                print(f"[ATM] PIN incorrecto. Intentos restantes: {restantes}.")
            else:
                print("[ATM] Demasiados intentos fallidos. La tarjeta será retenida.")
                self.intentos = 0
                atm.tarjeta = None
                atm.set_estado(atm.estado_sin_tarjeta)

    def consultar_saldo(self, atm) -> None:
        print("[ATM] Primero debe ingresar su PIN.")

    def extraer(self, atm, monto: float) -> None:
        print("[ATM] Primero debe ingresar su PIN.")

    def depositar(self, atm, monto: float) -> None:
        print("[ATM] Primero debe ingresar su PIN.")

    def retirar_tarjeta(self, atm) -> None:
        print("[ATM] Tarjeta retirada.")
        self.intentos = 0
        atm.tarjeta = None
        atm.set_estado(atm.estado_sin_tarjeta)
