from typing import Dict, List, Any, Optional
from entidad import Entidad

class Carrera(Entidad):
    def __init__(self, id: Optional[int] = None):
        super().__init__(id)
        self.nombre: str = ""
        self.codigo: str = ""
        self.descripcion: str = ""
        self.titulo: str = ""
        self.planes_estudio: List[Dict[str, Any]] = [] 


      
    