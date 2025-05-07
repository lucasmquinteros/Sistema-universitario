from datetime import date
from entidad import Entidad
from typing import Optional

class Examen(Entidad):
    def __init__(self, id: Optional[int] = None):
        super().__init__(id)
        self.tipo: str = ""
        self.fecha: Optional[date] = None
        self.nota: float = 0.0
        self.observaciones: str = ""
        self.id_profesor: Optional[int] = None
        self.id_profesor: str = ""

    def esta_aprobado(self) -> bool:
        return self.nota >= 6.0
    
    