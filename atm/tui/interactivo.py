import os

from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
import questionary

from atm import ATM
from atm.models.cuenta import Cuenta
from atm.models.tarjeta import Tarjeta
from atm.models.resultado_operacion import ResultadoOperacion

console = Console()

custom_style = questionary.Style([
    ("selected", "fg:cyan bold"),
    ("pointer", "fg:cyan bold"),
])

BANCO = "BANCO UNAB"


# ── Header ────────────────────────────────────────────────────────

def _limpiar() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _header(titulo: str, tarjeta: Tarjeta | None = None) -> None:
    """Header siempre visible. Muestra banco, pantalla actual y datos de sesión si hay tarjeta."""
    _limpiar()

    head =  """
++----------------------------------------------------------------++
++----------------------------------------------------------------++
||                                                                ||
|| ██╗   ██╗███╗   ██╗ █████╗ ██████╗  █████╗ ███╗   ██╗██╗  ██╗  ||
|| ██║   ██║████╗  ██║██╔══██╗██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝  ||
|| ██║   ██║██╔██╗ ██║███████║██████╔╝███████║██╔██╗ ██║█████╔╝   ||
|| ██║   ██║██║╚██╗██║██╔══██║██╔══██╗██╔══██║██║╚██╗██║██╔═██╗   ||
|| ╚██████╔╝██║ ╚████║██║  ██║██████╔╝██║  ██║██║ ╚████║██║  ██╗  ||
||  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝  ||
||                                                                ||
++----------------------------------------------------------------++
++----------------------------------------------------------------++
"""

    izquierda = Text(BANCO, style="bold yellow")
    derecha = Text()

    if tarjeta:
        derecha.append(tarjeta.cuenta.titular, style="bold cyan")
        derecha.append(f"  |  Saldo: ", style="dim")
        derecha.append(f"${tarjeta.cuenta.saldo:.2f}", style="bold green")
    else:
        derecha.append("Sin sesión activa", style="dim")

    console.print(head, style="cyan")
    console.print(Columns([izquierda, derecha], equal=True))
    console.rule(f"[dim]{titulo}[/dim]")
    console.print()


# ── Helpers ───────────────────────────────────────────────────────


def _mostrar_resultado(resultado: ResultadoOperacion) -> None:
    color = "green" if resultado.exito else "red"
    icono = "✓" if resultado.exito else "✗"
    console.print(Panel(
        f"[{color}]{icono} {resultado.mensaje}[/{color}]",
        border_style=color,
        expand=False,
    ))


def _continuar() -> None:
    questionary.press_any_key_to_continue(
        message="  Presione ENTER para continuar"
    ).ask()


def _pedir_monto(tarjeta: Tarjeta, pantalla: str) -> float | None:
    """Subpantalla para ingresar monto con opción de cancelar."""
    _header(pantalla, tarjeta)
    raw = questionary.text(
        "Ingrese monto:",
        validate=lambda v: True if v.replace(".", "", 1).isdigit() else "Ingrese un número válido"
    ).ask()

    if raw is None:
        return None
    return float(raw)


# ── Flujo login ───────────────────────────────────────────────────


def _flujo_login(tarjeta: Tarjeta, cajero: ATM) -> bool:
    """Inserta tarjeta y autentica PIN.

    Returns:
        True si autenticó correctamente.
        False si el usuario canceló o la tarjeta fue bloqueada.
    """
    _header("Insertar tarjeta")
    questionary.press_any_key_to_continue(
        message="  Presione ENTER para insertar tarjeta"
    ).ask()

    resultado = cajero.insertar_tarjeta(tarjeta)
    _mostrar_resultado(resultado)

    while True:
        _header("Ingrese su PIN")
        pin = questionary.password("  PIN:").ask()

        if pin is None:
            cajero.retirar_tarjeta()
            return False

        resultado = cajero.ingresar_pin(pin)
        _mostrar_resultado(resultado)

        if resultado.exito:
            _continuar()
            return True

        if tarjeta.bloqueada:
            console.print("\n[red bold]Tarjeta bloqueada. Comuníquese con su banco.[/red bold]")
            _continuar()
            cajero.retirar_tarjeta()
            return False

        _continuar()


# ── Flujos de operación ───────────────────────────────────────────

def _flujo_consultar(cajero: ATM, tarjeta: Tarjeta) -> None:
    _header("Consultar saldo", tarjeta)
    _mostrar_resultado(cajero.consultar_saldo())

    opcion = questionary.select(
        "  ¿Qué desea hacer?",
        choices=[
            "Depositar",
            "Extraer",
            questionary.Separator(),
            "← Volver",
        ],
        style=custom_style,
        use_indicator=True,
        pointer="▶ ",
        qmark="●",
    ).ask()

    if opcion == "Depositar":
        _flujo_depositar(cajero, tarjeta)
    elif opcion == "Extraer":
        _flujo_extraer(cajero, tarjeta)


def _flujo_depositar(cajero: ATM, tarjeta: Tarjeta) -> None:
    _header("Depositar", tarjeta)  # muestra saldo actual antes de depositar
    monto = questionary.text(
        "  Ingrese monto a depositar:",
        validate=lambda v: True if v.replace(".", "", 1).isdigit() else "Ingrese un número válido"
    ).ask()

    if monto is None:
        return

    _mostrar_resultado(cajero.depositar(float(monto)))
    _header("Depositar", tarjeta)  # refresca header con saldo actualizado
    questionary.print("  Depósito realizado con éxito.", style="green")
    opcion = questionary.select(
        "  ¿Qué desea hacer?",
        choices=[
            "Depositar otro monto",
            "Extraer",
            "Consultar saldo",
            questionary.Separator(),
            "← Volver al menú",
        ],
        style=custom_style,
        use_indicator=True,
        pointer="▶ ",
        qmark="●",
    ).ask()

    if opcion == "Depositar otro monto":
        _flujo_depositar(cajero, tarjeta)
    elif opcion == "Extraer":
        _flujo_extraer(cajero, tarjeta)
    elif opcion == "Consultar saldo":
        _flujo_consultar(cajero, tarjeta)


def _flujo_extraer(cajero: ATM, tarjeta: Tarjeta) -> None:
    _header("Extraer", tarjeta)  # muestra saldo disponible antes de extraer
    monto = questionary.text(
        "  Ingrese monto a extraer:",
        validate=lambda v: True if v.replace(".", "", 1).isdigit() else "Ingrese un número válido"
    ).ask()

    if monto is None:
        return

    if float(monto) > cajero.tarjeta.cuenta.saldo:
        questionary.print(" ❌ Saldo insuficiente para extraer ese monto. Ingrese un monto menor.", style="red")
        questionary.press_any_key_to_continue(message="  Presione ENTER para continuar").ask()
        _flujo_extraer(cajero, tarjeta)  # si el monto es mayor al saldo, no se permite extraer

    resultado = cajero.extraer(float(monto))
    _mostrar_resultado(resultado)
    _header("Extraer", tarjeta)  # refresca con saldo actualizado

    opciones = [
        "Extraer otro monto",
        "Depositar",
        "Consultar saldo",
        questionary.Separator(),
        "← Volver al menú",
    ]

    # si falló la extracción, ofrecer depositar primero
    if not resultado.exito:
        opciones = [
            "Depositar",
            "Consultar saldo",
            questionary.Separator(),
            "← Volver al menú",
        ]

    opcion = questionary.select(
        "  ¿Qué desea hacer?",
        choices=opciones,
        style=custom_style,
        use_indicator=True,
        pointer="▶ ",
        qmark="●",
    ).ask()

    if opcion == "Extraer otro monto":
        _flujo_extraer(cajero, tarjeta)
    elif opcion == "Depositar":
        _flujo_depositar(cajero, tarjeta)
    elif opcion == "Consultar saldo":
        _flujo_consultar(cajero, tarjeta)


# ── Flujo operaciones ─────────────────────────────────────────────


def _flujo_operaciones(cajero: ATM, tarjeta: Tarjeta) -> None:
    """Menú principal de operaciones. Se ejecuta mientras la sesión esté activa."""

    acciones = {
        "Consultar saldo":  lambda: _flujo_consultar(cajero, tarjeta),
        "Depositar":        lambda: _flujo_depositar(cajero, tarjeta),
        "Extraer":          lambda: _flujo_extraer(cajero, tarjeta),
    }

    while True:
        _header("Operaciones", tarjeta)

        opcion = questionary.select(
            "  Seleccione una operación",
            choices=[
                *acciones.keys(),
                questionary.Separator(),
                "← Finalizar sesión",
            ],
            style=custom_style,
            use_indicator=True,
            pointer="▶ ",
            qmark="●",
        ).ask()

        if opcion is None or opcion == "← Finalizar sesión":
            _header("Finalizar sesión", tarjeta)
            resultado = cajero.retirar_tarjeta()
            _mostrar_resultado(resultado)
            _continuar()
            return

        acciones[opcion]()


# ── Punto de entrada ──────────────────────────────────────────────


def interactivo(cuenta: Cuenta, tarjeta: Tarjeta, cajero: ATM) -> None:
    """Loop principal. Login → operaciones → vuelve al login."""

    while True:
        autenticado = _flujo_login(tarjeta, cajero)

        if not autenticado:
            _header("Salir")
            salir = questionary.confirm("  ¿Desea salir?").ask()
            if salir or salir is None:
                break
            continue

        _flujo_operaciones(cajero, tarjeta)

        _header("Sesión finalizada")
        otra = questionary.confirm("  ¿Desea iniciar otra sesión?").ask()
        if not otra:
            break

    console.print(Panel.fit(
        "[bold yellow]Gracias por usar BANCO UNAB. Hasta luego.[/bold yellow]",
        border_style="yellow"
    ))