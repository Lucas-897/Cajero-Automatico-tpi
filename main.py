from atm import ATM
from models import Cuenta, Tarjeta



if __name__ == "__main__":

    # CASO 1 - FLUJO NORMAL

    # --- Armado del escenario ---
    cuenta = Cuenta(titular="Juan Pérez", saldo=5000.00)
    tarjeta = Tarjeta(numero="1234-5678-9012-3456", pin= "1234", cuenta=cuenta)
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
    print("\n--- Historial de transacciones ---")
    for transaccion in cuenta.transacciones: 
        print(transaccion)
    
    # Fin de sesión
    print("\n--- Retirando tarjeta ---")
    cajero.retirar_tarjeta()

    # Intento de operar después de retirar la tarjeta
    print("\n--- Intentando operar sin tarjeta otra vez ---")
    cajero.consultar_saldo()

    print("\n" + "=" * 50)
    print("           FIN DE LA SIMULACIÓN")
    print("=" * 50)

 #CASO 2 - TRES PIN INCORRECTOS 


    print("\n" + "=" * 50)
    print("CASO 2 - TRES PIN INCORRECTOS")
    print("=" * 50)

    cuenta = Cuenta(titular="Ana López", saldo=3000.00)
    tarjeta = Tarjeta(numero="2222-3333-4444-5555", pin="4321", cuenta=cuenta)
    cajero = ATM()

    print("\n--- Insertando tarjeta ---")
    cajero.insertar_tarjeta(tarjeta)

    print("\n--- Ingresando PIN incorrecto 3 veces (bloqueo de tarjeta) ---")
    cajero.ingresar_pin("1111")
    cajero.ingresar_pin("2222")
    cajero.ingresar_pin("3333")

    print("\n--- Intentando operar luego del bloqueo ---")
    cajero.consultar_saldo()
    cajero.extraer(500)
    cajero.depositar(1000)
 

 # CASO 3 - OPERACIONES DESPUÉS DE BLOQUEO

    print("\n" + "=" * 50)
    print("CASO 3 - NUEVA TARJETA")
    print("=" * 50)

    cuenta2 = Cuenta(titular="María García", saldo=8000.00)
    tarjeta2 = Tarjeta(numero="9999-8888-7777-6666", pin="5678", cuenta=cuenta2)

    print("\n--- Insertando nueva tarjeta ---")
    cajero.insertar_tarjeta(tarjeta2)

    print("\n--- Ingresando PIN correcto ---")
    cajero.ingresar_pin("5678")

    print("\n--- Operando normalmente ---")
    cajero.consultar_saldo()
    cajero.depositar(500)
    cajero.extraer(1000)
    cajero.consultar_saldo()

    print("\n--- Retirando tarjeta ---")
    cajero.retirar_tarjeta()

    print("\n" + "=" * 50)
    print("       FIN DE LA SIMULACIÓN")
    print("=" * 50)