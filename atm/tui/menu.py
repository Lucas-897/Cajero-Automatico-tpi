from rich.console import Console
from rich.panel import Panel
from rich.table import Table
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
    console.rule(f"[bold cyan]{titulo}[/bold cyan]")


def _header() -> None:
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

    console.print(Panel.fit("[bold green]FIN DE LA SIMULACIÓN[/bold green]", border_style="green"))


# ── Modo interactivo ──────────────────────────────────────────────


def interactivo(cuenta: Cuenta, tarjeta: Tarjeta, cajero: ATM) -> None:
    """Menú interactivo: el usuario elige cada operación."""
    _header()
    console.print("[dim]Tarjeta disponible para insertar: 1234-5678-9012-3456 | PIN: 1234[/dim]\n")

    opciones = {
        "1": ("Insertar tarjeta",   lambda: cajero.insertar_tarjeta(tarjeta)),
        "2": ("Ingresar PIN",       lambda: cajero.ingresar_pin(console.input("  [cyan]PIN:[/cyan] "))),
        "3": ("Consultar saldo",    lambda: cajero.consultar_saldo()),
        "4": ("Depositar",          lambda: cajero.depositar(float(console.input("  [cyan]Monto:[/cyan] ")))),
        "5": ("Extraer",            lambda: cajero.extraer(float(console.input("  [cyan]Monto:[/cyan] ")))),
        "6": ("Retirar tarjeta",    lambda: cajero.retirar_tarjeta()),
        "0": ("Salir",              None),
    }

    while True:
        _seccion("Menú")
        table = Table(show_header=False, box=None, padding=(0, 2))
        for key, (label, _) in opciones.items():
            table.add_row(f"[bold cyan]{key}[/bold cyan]", label)
        console.print(table)

        eleccion = console.input("\n  [bold]Opción:[/bold] ").strip()

        if eleccion not in opciones:
            console.print("  [red]Opción inválida.[/red]")
            continue

        label, accion = opciones[eleccion]

        if accion is None:
            console.print("\n[bold yellow]Hasta luego.[/bold yellow]")
            break

        try:
            resultado = accion()
            _mostrar(label, resultado)
        except ValueError:
            console.print("  [red]✗ Ingresá un número válido.[/red]")

        console.print()