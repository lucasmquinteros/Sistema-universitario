from entidad import Entidad
from typing import Optional, List, Dict

class Rol(Entidad):
    def __init__(self, id: Optional[int] = None):
        super().__init__(id)
        self.nombre: str = ""
        self.descripcion: str = ""
        self.permisos: List[Dict[str, str]] = []

    
