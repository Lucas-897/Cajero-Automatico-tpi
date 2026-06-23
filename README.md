# Cajero-Automatico-tpi

Simulación de un cajero automático desarrollada en Python como Trabajo Práctico Integrador de la materia **Programación Avanzada**.

---

## Descripción

El sistema modela el comportamiento de un cajero automático real, donde las operaciones disponibles dependen del **estado actual** de la sesión. Un usuario solo puede operar si insertó su tarjeta y validó su PIN correctamente.

---

## Conceptos aplicados

- **Programación Orientada a Objetos**: encapsulamiento, abstracción, herencia y polimorfismo.
- **Patrón de Diseño State**: el cajero delega cada acción al estado actual, cambiando su comportamiento sin modificar la clase principal.
- **Composición**: `Tarjeta` contiene una `Cuenta`, `Cuenta` contiene una lista de `Transaccion`.
- **Clases abstractas**: `EstadoATM` define la interfaz que todos los estados deben implementar.

---

## Estructura del proyecto

```
cajero-automatico-tpi/
├── main.py                  # Punto de entrada y escenario de demostración
├── atm.py                   # Clase principal, delega al estado actual
├── models/
│   ├── cuenta.py            # Saldo, extracción y depósito
│   ├── tarjeta.py           # Número, PIN y referencia a Cuenta
│   └── transaccion.py       # Registro de cada operación realizada
└── states/
    ├── estado_atm.py        # Interfaz abstracta (ABC)
    ├── sin_tarjeta.py       # Bloquea todo menos insertar tarjeta
    ├── tarjeta_insertada.py # Maneja intentos de PIN
    └── autenticado.py       # Permite consultar saldo, extraer y depositar
```

---

## Estados del cajero

| Estado | Descripción |
|---|---|
| `SinTarjeta` | Estado inicial. Solo permite insertar tarjeta. |
| `TarjetaInsertada` | Espera el PIN. Retiene la tarjeta tras 3 intentos fallidos. |
| `Autenticado` | Permite consultar saldo, extraer y depositar. |

---

## Cómo ejecutar


```bash
# Clonar el repositorio
git clone https://github.com/Lucas-897/Cajero-Automatico-tpi.git

# Entrar a la carpeta
cd Cajero-Automatico-tpi

# Ejecutar
python main.py
```

---

## Ejemplo de salida

```
==================================================
        SIMULACIÓN DE CAJERO AUTOMÁTICO
==================================================

--- Intentando operar sin tarjeta ---
[ATM] Primero debe insertar una tarjeta.

--- Insertando tarjeta ---
[ATM] Tarjeta insertada. Por favor ingrese su PIN.

--- Ingresando PIN incorrecto ---
[ATM] PIN incorrecto. Intentos restantes: 2.
[ATM] PIN incorrecto. Intentos restantes: 1.

--- Ingresando PIN correcto ---
[ATM] PIN correcto. Bienvenido/a.

--- Operaciones disponibles ---
[ATM] Titular: Juan Pérez | Saldo disponible: $5000.00
[ATM] Depósito exitoso de $2000.00.
[ATM] Titular: Juan Pérez | Saldo disponible: $7000.00
[ATM] Extracción exitosa de $1500.00. Retire su dinero.
[ATM] Titular: Juan Pérez | Saldo disponible: $5500.00
[ERROR] Saldo insuficiente.

--- Retirando tarjeta ---
[ATM] Sesión finalizada. Retire su tarjeta. ¡Hasta luego!
```

---

## Integrantes

- Arbona Yasmin
- Micaela Cafardo
- Juan Esparza
- Lucas Colosimo
