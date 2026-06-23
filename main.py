from atm import ATM
from models.cuenta import Cuenta
from models.tarjeta import Tarjeta


if __name__ == "__main__":

    # --- Armado del escenario ---
    cuenta = Cuenta(titular="Juan Pérez", saldo=5000.00)
    tarjeta = Tarjeta(numero="1234-5678-9012-3456", pin="1234", cuenta=cuenta)
    cajero = ATM()

    print("=" * 50)
    print("        SIMULACIÓN DE CAJERO AUTOMÁTICO")
    print("=" * 50)

    # Intento de operar sin tarjeta
    print("\n--- Intentando operar sin tarjeta ---")
    cajero.consultar_saldo()
    cajero.extraer(100)

    # Inserción de tarjeta
    print("\n--- Insertando tarjeta ---")
    cajero.insertar_tarjeta(tarjeta)

    # PIN incorrecto
    print("\n--- Ingresando PIN incorrecto ---")
    cajero.ingresar_pin("0000")
    cajero.ingresar_pin("9999")

    # PIN correcto
    print("\n--- Ingresando PIN correcto ---")
    cajero.ingresar_pin("1234")

    # Operaciones autenticadas
    print("\n--- Operaciones disponibles ---")
    cajero.consultar_saldo()

    cajero.depositar(2000)
    cajero.consultar_saldo()

    cajero.extraer(1500)
    cajero.consultar_saldo()

    cajero.extraer(99999)  # saldo insuficiente

    # Fin de sesión
    print("\n--- Retirando tarjeta ---")
    cajero.retirar_tarjeta()

    # Intento de operar después de retirar la tarjeta
    print("\n--- Intentando operar sin tarjeta otra vez ---")
    cajero.consultar_saldo()

    print("\n" + "=" * 50)
    print("           FIN DE LA SIMULACIÓN")
    print("=" * 50)
