from states.estado_atm import EstadoATM


class Autenticado(EstadoATM):

    def insertar_tarjeta(self, atm) -> None:
        print("[ATM] Ya hay una sesión activa.")

    def ingresar_pin(self, atm, pin: str) -> None:
        print("[ATM] Ya está autenticado/a.")

    def consultar_saldo(self, atm) -> None:
        saldo = atm.tarjeta.cuenta.saldo
        titular = atm.tarjeta.cuenta.titular
        print(f"[ATM] Titular: {titular} | Saldo disponible: ${saldo:.2f}")

    def extraer(self, atm, monto: float) -> None:
        exito = atm.tarjeta.cuenta.extraer(monto)
        if exito:
            print(f"[ATM] Extracción exitosa de ${monto:.2f}. Retire su dinero.")

    def depositar(self, atm, monto: float) -> None:
        exito = atm.tarjeta.cuenta.depositar(monto)
        if exito:
            print(f"[ATM] Depósito exitoso de ${monto:.2f}.")

    def retirar_tarjeta(self, atm) -> None:
        print("[ATM] Sesión finalizada. Retire su tarjeta. ¡Hasta luego!")
        atm.tarjeta = None
        atm.set_estado(atm.estado_sin_tarjeta)
