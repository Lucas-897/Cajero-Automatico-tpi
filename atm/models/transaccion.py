from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


class TipoTransaccion(Enum):
    """Tipos válidos de transacción. Usar estos valores evita errores de tipeo y restringe
    las operaciones posibles a las que el sistema conoce."""
    DEPOSITO = "DEPOSITO"
    EXTRACCION = "EXTRACCION"


@dataclass(frozen=True)
class Transaccion:
    """Representa un movimiento bancario ya ocurrido (depósito, extracción, etc.).
    
    Es inmutable (frozen=True): una transacción es un hecho del pasado,
    no se puede modificar después de crearse.
    """
    tipo: TipoTransaccion
    monto: float
    fecha: datetime = field(default_factory=datetime.now)

    def __str__(self):
        """Ej: [24/06/2025 14:32:01] DEPOSITO: $1500.00"""
        return f"[{self.fecha.strftime('%d/%m/%Y %H:%M:%S')}] {self.tipo.value}: ${self.monto:.2f}"