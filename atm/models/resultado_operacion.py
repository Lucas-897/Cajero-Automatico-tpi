from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoOperacion:
    """Resultado de cualquier operación del ATM.
    
    Separa la lógica de negocio de la presentación:
    los estados devuelven esto, el menú decide cómo mostrarlo.
    """
    exito: bool
    mensaje: str