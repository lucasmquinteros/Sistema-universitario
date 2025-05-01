from datetime import date
from typing import List, Dict, Any, Optional
from .entidad import Entidad

class Alumno(Entidad):
    def __init__(self, id: Optional[int] = None):
        super().__init__(id)
        self.nombre: str = ""
        self.apellido: str = ""
        self.dni: str = ""
        self.fecha_nacimiento: date = None
        self.email: str = ""
        self.telefono: Optional[str] = None
        self.direccion: Optional[str] = None
        self.fecha_ingreso: date = date.today()
        self.estado: str = "Activo"
        self.carreras: List[Dict[str, Any]] = []
        self.cursadas: List[Dict[str, Any]] = []
    
    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"
    
    def esta_inscripto_en_carrera(self, carrera_id: int) -> bool:
        return any(c['id'] == carrera_id for c in self.carreras)
    
    def esta_cursando(self, asignatura_id: int) -> bool:
        return any(c['id'] == asignatura_id and c['estado'] == 'Cursando' 
                  for c in self.cursadas)