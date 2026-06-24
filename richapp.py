import time
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text

console = Console()


choices = [
        "💰  Consultar saldo",
        "💸  Extraer dinero",
        "📥  Depositar",
        "🚪  Salir",
]

def get_user_choice(choices=choices):
    return questionary.select(
        "¿Qué operación desea realizar?",
        choices=choices,
    ).ask()



def ingresar_pin(longitud=4):
    pin = questionary.password("Ingrese su PIN:").ask()
    console.print()
    return pin


def barra_proceso(mensaje="Procesando", demora=1.5):
    with Progress(transient=True) as progress:
        task = progress.add_task(f"[cyan]{mensaje}...", total=100)
        while not progress.finished:
            time.sleep(demora / 50)
            progress.advance(task, 2)


# ── Pantalla de bienvenida ──────────────────────────────────────────────────
console.clear()
console.print(
    Panel(
        "[bold yellow]🏧  CAJERO AUTOMÁTICO[/bold yellow]\n[dim]Banco Demo SA[/dim]",
        expand=False,
        border_style="yellow",
    )
)

# ── Ingreso de tarjeta (simulado) ───────────────────────────────────────────
console.print("\n[dim]Inserte su tarjeta...[/dim]")
barra_proceso("Leyendo tarjeta", demora=1)
console.print("[green]✓ Tarjeta reconocida[/green]\n")

# ── PIN ─────────────────────────────────────────────────────────────────────
console.print("[bold]Ingrese su PIN:[/bold]")
pin = ingresar_pin(longitud=4)

barra_proceso("Validando PIN", demora=1)

if pin == "1234":  # PIN hardcodeado para demo
    console.print("[green]✓ PIN correcto[/green]\n")
else:
    console.print("[red]✗ PIN incorrecto. Tarjeta bloqueada.[/red]")
    raise SystemExit

# ── Menú principal ───────────────────────────────────────────────────────────
operacion = questionary.select(
    "¿Qué operación desea realizar?",
    choices=[
        "💰  Consultar saldo",
        "💸  Extraer dinero",
        "📥  Depositar",
        "🚪  Salir",
    ],
).ask()

barra_proceso("Procesando operación", demora=1.2)

session = True
while session:
    operacion = get_user_choice(choices=choices)

    if operacion == "💰  Consultar saldo":
        console.print("[bold green]Su saldo actual es: $1,000.00[/bold green]\n")

    elif operacion == "💸  Extraer dinero":
        monto = questionary.text("Ingrese monto a extraer: $").ask()
        barra_proceso("Dispensando billetes", demora=2)
        console.print(
            Panel(
                f"[bold green]Entregando $ {monto}[/bold green]\n[dim]Retire sus billetes[/dim]",
                border_style="green",
                expand=False,
            )
        )

    elif operacion == "📥  Depositar":
        monto = questionary.text("Ingrese monto a depositar: $").ask()
        barra_proceso("Acreditando depósito", demora=1.5)
        console.print(
            Panel(
                f"[bold green]Depósito acreditado: $ {monto}[/bold green]",
                border_style="green",
                expand=False,
            )
        )

    elif operacion == "🚪  Salir":
        confirm = questionary.confirm("¿Desea finalizar la sesión?").ask()
        if confirm:
            console.print(
                "[bold yellow]Gracias por usar nuestro cajero automático. ¡Hasta luego![/bold yellow]"
            )
            session = False
            break
