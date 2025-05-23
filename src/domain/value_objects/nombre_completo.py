from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class NombreCompleto:
    """Value Object que representa un nombre completo de una persona"""

    nombre: str
    apellido: str
    segundo_nombre: Optional[str] = None

    def __str__(self) -> str:
        """Representación en string del nombre completo"""
        if self.segundo_nombre:
            return f"{self.nombre} {self.segundo_nombre} {self.apellido}"
        return f"{self.nombre} {self.apellido}"

    def iniciales(self) -> str:
        """Retorna las iniciales del nombre completo"""
        if self.segundo_nombre:
            return f"{self.nombre[0]}{self.segundo_nombre[0]}{self.apellido[0]}"
        return f"{self.nombre[0]}{self.apellido[0]}"
