from states.estado_atm import EstadoATM


class TarjetaInsertada(EstadoATM):

    def insertar_tarjeta(self, atm) -> None:
        print("[ATM] Ya hay una tarjeta insertada.")

    def ingresar_pin(self, atm, pin: str) -> None:
        if atm.tarjeta.validar_pin(pin):
            atm.resetear_intentos()
            print("[ATM] PIN correcto. Bienvenido/a.")
            atm.set_estado(atm.estado_autenticado) # cambio de estado a autenticado (tarjeta + pin ok)
        else:
            intentos_agotados = atm.registrar_intento_fallido()
            if intentos_agotados:  # Se agotaron los intentos
                print("[ATM] Demasiados intentos. Tarjeta bloqueada.")
                atm.tarjeta.bloquear() #    bloquear tarjeta
                atm.tarjeta = None # Tragarse la tarjeta (quitarla)
                atm.resetear_intentos()
                atm.set_estado(atm.estado_sin_tarjeta) # Cambio de estado a sin tarjeta.
            else:
                print(f"[ATM] PIN incorrecto. Intentos restantes: {atm.intentos_restantes()}.")

    def consultar_saldo(self, atm) -> None:
        print("[ATM] Primero debe ingresar su PIN.")

    def extraer(self, atm, monto: float) -> None:
        print("[ATM] Primero debe ingresar su PIN.")

    def depositar(self, atm, monto: float) -> None:
        print("[ATM] Primero debe ingresar su PIN.")

    def retirar_tarjeta(self, atm) -> None:
        print("[ATM] Tarjeta retirada.")
        atm.resetear_intentos()
        atm.tarjeta = None
        atm.set_estado(atm.estado_sin_tarjeta)