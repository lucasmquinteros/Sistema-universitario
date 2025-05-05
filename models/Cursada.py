from typing import Optional, List, Dict, Any
from datetime import date
from entidad import Entidad

class Cursada(Entidad):
    def __init__(self, id: Optional[int] = None): 
        super().__init__(id)
        self.id_alumno: Optional[int] = None
        self.id_asignatura: Optional[int] = None
        self.anio: int = 0
        self.cuatrimestre: int = 0
        self.estado: str = ""
        self.fecha_inscripcion: Optional[date] = None
        self.notas: List[Dict[str, Any]] = []

    def getPromedio(self) -> float:
        if not self.notas:
            return 0.0
        suma_notas = sum(nota['valor'] for nota in self.notas)
        return suma_notas / len(self.notas)
    def getEstado(self) -> str:
        nota = self.getPromedio()
        if nota >= 6:
            return "Aprobada"
        elif nota >= 4:
            return "Regular"
        else:
            return "Desaprobada"