from typing import List, Dict, Any, Optional
from .entidad import Entidad

class Usuario(Entidad):
    def __init__(self, id: Optional[int] = None):
        super().__init__(id)
        self.nombre_usuario: str = ""
        self.roles: List[Dict[str, Any]] = [] 

    def tiene_permiso(self, codigo: str) -> bool:
        return any(codigo in rol['permisos'] for rol in self.roles)