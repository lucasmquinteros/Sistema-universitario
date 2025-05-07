from entidad import Entidad
from typing import Optional
class Permiso(Entidad):
    def __init__(self, id: Optional[int] = None):
        super().__init__(id)
        self.codigo: str = ""
        self.descripcion: str = ""
        self.modulo: str = ""

    