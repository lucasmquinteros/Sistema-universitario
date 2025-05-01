from typing import List, Dict, Any, Optional
from .entidad import Entidad

class Profesor(Entidad):
    def __init__(self, id: Optional[id] = None): 
        super().__init__(id),
        self.nombre: str = "",
        self.apellido: str = "",
        self.dni: str = "",
        self.email: str = ""
        self.telefono: Optional[str] = None
        self.titulo: str = "",
        self.especialidad: Optional[str] = "",
        self.departamento: str = ""
        

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

