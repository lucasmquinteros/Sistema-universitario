# sistema_universitario/models/asignatura.py
from typing import Optional, List, Dict, Any
from .entidad import Entidad

class Asignatura(Entidad):    
    def __init__(self, id: Optional[int] = None):
        super().__init__(id)
        self.nombre: str = ""
        self.hsemanal: int = 0  
        self.htotales: int = 0  
        self.creditos: int = 0
        
        
        self.id_area: Optional[int] = None
        self.area: Optional[str] = None  
        self.id_regimen: Optional[int] = None
        self.regimen: Optional[str] = None  
        self.id_depto: Optional[int] = None
        self.departamento: Optional[str] = None  
        
        
        self.profesores: List[Dict[str, Any]] = []
        self.correlativas: List[Dict[str, Any]] = []
        self.planes_estudio: List[Dict[str, Any]] = []
    
    @property
    def es_cuatrimestral(self) -> bool:
        return self.regimen and "cuatrimestral" in self.regimen.lower()
    
    @property
    def es_anual(self) -> bool:
        return self.regimen and "anual" in self.regimen.lower()
    
    def tiene_correlativas(self) -> bool:
        return len(self.correlativas) > 0
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.creditos} créditos)"