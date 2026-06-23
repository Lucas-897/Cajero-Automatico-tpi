from atm import ATM
from atm.models import Cuenta, Tarjeta
from atm.tui import menu


if __name__ == "__main__":

    # --- Armado del escenario ---
    cuenta = Cuenta(titular="Juan Pérez", saldo=5000.00)
    tarjeta = Tarjeta(numero="1234-5678-9012-3456", pin= "1234", cuenta=cuenta)
    cajero = ATM()

    menu.test_no_interactivo(cuenta, tarjeta, cajero)
