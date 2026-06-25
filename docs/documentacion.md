# Simulador de Cajero Automático

## Introducción

Este trabajo presenta un simulador de cajero automático desarrollado en Python con enfoque orientado a objetos. La aplicación permite insertar una tarjeta, validar un PIN, consultar saldo, realizar depósitos, hacer extracciones y retirar la tarjeta desde la terminal.

La intención del proyecto no fue solamente que el cajero funcionara, sino modelar su comportamiento de forma clara y extensible. Por eso se separó la lógica en clases de dominio y clases de comportamiento, apoyándose en conceptos de Programación Orientada a Objetos y en el patrón de diseño `State`.

## Tema

El tema central es la simulación de una sesión de cajero automático con control de acceso y reglas distintas según el estado de uso.

En un cajero real no todas las acciones están siempre disponibles. Antes de insertar una tarjeta no tiene sentido consultar saldo. Antes de validar el PIN no se deberían permitir extracciones ni depósitos. Si el PIN falla demasiadas veces, la tarjeta debe bloquearse. El sistema reproduce justamente esa lógica.

## Problema

El problema principal consiste en representar un objeto que cambia su comportamiento según la etapa de la sesión.

Una solución basada en muchos `if` y `elif` dentro de una sola clase habría funcionado al principio, pero rápidamente se volvería difícil de mantener. Cada operación tendría que preguntar en qué estado se encuentra el cajero, y eso mezclaría reglas de negocio con control de flujo.

Además del cambio de comportamiento, el proyecto debía resolver otros puntos:

- Proteger datos sensibles como el PIN, el saldo y el estado de bloqueo.
- Registrar movimientos de la cuenta.
- Permitir el bloqueo de tarjeta luego de varios intentos fallidos.
- Mantener separada la interfaz de salida respecto de la lógica principal.

## Solución

La solución elegida fue dividir el sistema en clases con responsabilidades concretas:

- `ATM` coordina la sesión y delega el comportamiento al estado activo.
- `EstadoATM` define el contrato común de operaciones.
- `SinTarjeta`, `TarjetaInsertada` y `Autenticado` representan las etapas de uso del cajero.
- `Tarjeta` modela la credencial del usuario y su validación.
- `Cuenta` almacena el saldo y los movimientos.
- `Transaccion` registra cada operación realizada.

Esta estructura permite que el cajero cambie de comportamiento sin reescribir la lógica general. El objeto `ATM` no decide todo por sí mismo; actúa como un coordinador que deriva cada acción al estado correspondiente.

La alternativa descartada fue concentrar todo en una única clase con control condicional por operación. Esa opción hubiera sido más corta al inicio, pero menos clara, menos escalable y más difícil de probar.

## Diagrama y diseño

El modelo de clases está documentado en [`docs/uml.md`](/docs/uml.md) y representado visualmente en [`docs/uml.png`](/docs/uml.png).

El diagrama muestra las relaciones principales del sistema y deja ver que el proyecto supera el mínimo de clases requeridas. También permite distinguir qué parte pertenece al dominio y cuál al comportamiento del cajero.

### Lectura del diseño

- `ATM` mantiene la sesión activa y el estado actual.
- `EstadoATM` funciona como base abstracta para que todos los estados compartan la misma interfaz.
- `Tarjeta` se asocia a una `Cuenta`.
- `Cuenta` compone un conjunto de `Transaccion`.

La decisión de separar estas responsabilidades responde a una idea simple: cada clase debe tener un objetivo claro. Así, el código queda más legible y cada parte del sistema puede evolucionar sin romper el resto.

## Conceptos de POO

### Encapsulamiento

Se utilizó encapsulamiento para proteger los datos más sensibles:

- `Cuenta` oculta `_titular`, `_saldo` y `_transacciones`.
- `Tarjeta` oculta `_pin` y `_bloqueada`.
- `ATM` oculta `_estado_actual` y el contador de intentos de PIN.

La alternativa descartada fue dejar esos atributos públicos y permitir acceso directo desde cualquier parte del programa. Esa opción simplifica el acceso, pero debilita el control sobre el estado interno y facilita errores como modificar el saldo sin validación.

### Abstracción

La clase `EstadoATM` define una interfaz común para las acciones del cajero. No implementa la lógica concreta, pero establece qué operaciones deben existir en cualquier estado.

Esto permite que `ATM` trabaje contra una abstracción y no contra clases concretas. La decisión ayuda a ordenar el diseño y a reducir dependencias directas.

### Herencia

`SinTarjeta`, `TarjetaInsertada` y `Autenticado` heredan de `EstadoATM`.

Se eligió herencia porque los tres estados responden al mismo contrato, aunque con comportamientos distintos. Una alternativa sería repetir métodos en clases independientes sin base común, pero eso duplicaría estructura y dificultaría el mantenimiento.

### Polimorfismo

El polimorfismo aparece cuando `ATM` invoca siempre la misma operación y el resultado cambia según el estado activo.

Por ejemplo, `consultar_saldo()` no hace lo mismo en `SinTarjeta` que en `Autenticado`. En un caso informa que primero se debe insertar la tarjeta; en el otro muestra el saldo disponible. La llamada es la misma, pero el comportamiento varía.

## Patrón State

El patrón `State` es la decisión de diseño más importante del proyecto.

El cajero puede estar en tres estados principales:

- `SinTarjeta`
- `TarjetaInsertada`
- `Autenticado`

Cada estado encapsula las reglas válidas para ese momento. Cuando cambia la etapa de la sesión, `ATM` cambia la referencia al objeto estado correspondiente. Así se evita llenar la clase principal con condicionales y se hace más sencillo agregar estados nuevos en el futuro.

La alternativa descartada fue resolver todo con banderas internas y bloques `if` en cada método. Ese enfoque habría mezclado validación, transición de estados y lógica de negocio en el mismo lugar.

## Decisiones de diseño

| Decisión | Motivo | Alternativa descartada |
|---|---|---|
| Separar `ATM` y los estados | Cada etapa del cajero tiene reglas distintas | Una sola clase con muchos condicionales |
| Encapsular saldo, PIN y bloqueo | Protege información sensible y evita cambios accidentales | Atributos públicos con acceso directo |
| Usar `EstadoATM` como clase abstracta | Obliga a mantener una interfaz común | Repetir métodos sin contrato compartido |
| Registrar transacciones en `Cuenta` | Deja trazabilidad de los movimientos | Manejar el historial fuera del modelo de dominio |
| Asociar `Tarjeta` con `Cuenta` | Representa la relación real entre credencial y cuenta | Tratar tarjeta y cuenta como objetos totalmente aislados |
| Manejar intentos de PIN en `ATM` | Centraliza el control de sesión | Repartir el conteo de intentos entre varios estados |

## Cobertura del trabajo

El proyecto refleja los puntos esperables de la consigna de forma integrada:

- Presenta un diagrama de clases con las clases principales y sus relaciones.
- Usa más de tres clases de dominio y comportamiento.
- Aplica encapsulamiento, abstracción, herencia y polimorfismo.
- Incluye un patrón de diseño real y visible en ejecución.
- Se puede demostrar desde `main.py` con un flujo completo de uso.

## Demostración

La ejecución de `main.py` muestra un recorrido completo de uso:

1. Se crea una cuenta con saldo inicial.
2. Se asocia una tarjeta a esa cuenta.
3. Se intenta operar sin tarjeta para mostrar las restricciones.
4. Se inserta la tarjeta.
5. Se ingresan PINes incorrectos.
6. Se ingresa el PIN correcto y el sistema pasa a estado autenticado.
7. Se consulta el saldo.
8. Se realiza un depósito.
9. Se realiza una extracción.
10. Se imprime el historial de transacciones.
11. Se retira la tarjeta y el cajero vuelve al estado inicial.

Esto permite mostrar en defensa que el comportamiento no está simulado solo con texto, sino modelado mediante objetos y estados reales.

## Cierre

El resultado final es un programa sencillo de ejecutar, pero con una estructura técnica clara. La división entre dominio, estados y coordinación hace que el sistema sea comprensible y extensible.

En síntesis, el proyecto cumple su objetivo funcional y, al mismo tiempo, sirve como ejemplo concreto de aplicación de POO y del patrón `State` en un caso de uso cercano a la realidad.
