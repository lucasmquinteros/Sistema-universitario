from typing import Optional, List, Dict, Any
from datetime import date
from .entidad import Entidad

class Profesor(Entidad):
    """Clase que representa a un profesor en el sistema"""
    
    def __init__(self, id: Optional[int] = None):
        super().__init__(id)
        # Atributos básicos
        self.nombre: str = ""
        self.apellido: str = ""
        self.dni: str = ""
        self.email: str = ""
        self.telefono: Optional[str] = None
        
        # Atributos profesionales
        self.titulo: str = ""
        self.especialidad: Optional[str] = None
        self.tipo_contrato: str = ""
        self.fecha_ingreso: date = date.today()
        
        # Relaciones
        self.id_departamento: Optional[int] = None
        self.departamento: Optional[str] = None  # Nombre del departamento (para mostrar)
        self.asignaturas: List[Dict[str, Any]] = []
    
    @property
    def nombre_completo(self) -> str:
        """Devuelve el nombre completo del profesor"""
        return f"{self.nombre} {self.apellido}"
    
    def asignar_departamento(self, id_departamento: int, nombre_departamento: Optional[str] = None) -> None:
        """Asigna un departamento al profesor"""
        self.id_departamento = id_departamento
        if nombre_departamento:
            self.departamento = nombre_departamento
    
    def es_titular(self) -> bool:
        """Verifica si el profesor es titular"""
        return self.tipo_contrato.lower() == "titular"
    
    def __str__(self) -> str:
        """Representación en string del profesor"""
        return f"{self.nombre_completo} - {self.titulo}"