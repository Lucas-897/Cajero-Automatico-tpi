import questionary
from rich.console import Console
from rich.panel import Panel
from atm.models.resultado_operacion import ResultadoOperacion
from atm.models.cuenta import Cuenta
from atm.models.tarjeta import Tarjeta
from atm import ATM

console = Console()


# ── Helpers de presentación ───────────────────────────────────────
def _mostrar(operacion: str, resultado: ResultadoOperacion) -> None:
    """Imprime la operación intentada y su resultado con color."""
    color = "green" if resultado.exito else "red"
    icono = "✓" if resultado.exito else "✗"
    console.print(f"  [dim]>{' ' + operacion}[/dim]")
    console.print(f"  [{color}]{icono} {resultado.mensaje}[/{color}]")


def _seccion(titulo: str) -> None:
    questionary.print(titulo, style="bold cyan")


def _header() -> None:
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
    console.print(head, style="cyan")
    console.print(Panel.fit(
        "[bold yellow]SIMULADOR DE CAJERO AUTOMÁTICO[/bold yellow]",
        border_style="yellow"
    ))


# ── Modo automático ───────────────────────────────────────────────


def automatico(cuenta: Cuenta, tarjeta: Tarjeta, cajero: ATM) -> None:
    """Demo automática: ejecuta un escenario fijo sin input del usuario."""
    _header()

    _seccion("Sin tarjeta insertada")
    _mostrar("consultar saldo", cajero.consultar_saldo())
    _mostrar("extraer $100", cajero.extraer(100))

    _seccion("Inserción de tarjeta")
    _mostrar("insertar tarjeta", cajero.insertar_tarjeta(tarjeta))

    _seccion("Intentos de PIN incorrectos")
    _mostrar("ingresar PIN 0000", cajero.ingresar_pin("0000"))
    _mostrar("ingresar PIN 9999", cajero.ingresar_pin("9999"))

    _seccion("PIN correcto")
    _mostrar("ingresar PIN 1234", cajero.ingresar_pin("1234"))

    _seccion("Operaciones autenticadas")
    _mostrar("consultar saldo", cajero.consultar_saldo())
    _mostrar("depositar $2000", cajero.depositar(2000))
    _mostrar("consultar saldo", cajero.consultar_saldo())
    _mostrar("extraer $1500", cajero.extraer(1500))
    _mostrar("consultar saldo", cajero.consultar_saldo())
    _mostrar("extraer $99999 (insuficiente)", cajero.extraer(99999))

    _seccion("Fin de sesión")
    _mostrar("retirar tarjeta", cajero.retirar_tarjeta())

    _seccion("Post-sesión")
    _mostrar("consultar saldo", cajero.consultar_saldo())
