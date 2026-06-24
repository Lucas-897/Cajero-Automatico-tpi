import sys
from atm import ATM
from atm.models import Cuenta, Tarjeta
from atm.tui import menu


if __name__ == "__main__":
    cuenta = Cuenta(titular="Juan Pérez", saldo_inicial=5000.00)
    tarjeta = Tarjeta(numero="1234-5678-9012-3456", pin="1234", cuenta=cuenta)
    cajero = ATM()

    modo = sys.argv[1] if len(sys.argv) > 1 else "interactivo"

    if modo == "auto":
        menu.automatico(cuenta, tarjeta, cajero)
    else:
        menu.menu(cuenta, tarjeta, cajero)
