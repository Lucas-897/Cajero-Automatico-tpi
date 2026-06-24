import questionary
from prompt_toolkit.styles import Style
from atm.tui.interactivo import interactivo
from atm.tui.automatico import automatico
from atm.models.cuenta import Cuenta
from atm.models.tarjeta import Tarjeta
from atm import ATM

custom_style = Style([
    ("selected", "fg:cyan bold"),
    ("pointer", "fg:cyan bold"),
])


def menu(cuenta: Cuenta, tarjeta: Tarjeta, cajero: ATM) -> None:
    """Muestra el menú principal y permite elegir entre modo automático o interactivo."""
    opcion = questionary.select(
        "Seleccione un modo de operación",
        choices=[
            "Modo automático (demo)",
            "Modo interactivo",
            questionary.Separator(),
            "Salir",
        ],
        style=custom_style,
        use_indicator=True,
        pointer="▶ ",
        qmark="●",
    ).ask()

    if opcion is None or opcion == "Salir":
        return

    if opcion == "Modo automático (demo)":
        automatico(cuenta, tarjeta, cajero)
    elif opcion == "Modo interactivo":
        interactivo(cuenta, tarjeta, cajero)
