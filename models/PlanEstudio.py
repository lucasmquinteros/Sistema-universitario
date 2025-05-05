from typing import Dict, List, Any
class PlanEstudio:
        
    def __init__(self, nombre: str, codigo: str, id_carrera: int, carrera: str, vigente: bool, asignaturas: List[Dict[str, Any]]):
        self.nombre = nombre
        self.codigo = codigo
        self.id_carrera = id_carrera
        self.carrera = carrera
        self.vigente = vigente
        self.asignaturas = asignaturas 

    def obtenerAsignaturasPorAnio(self, anio: int) -> List[Dict[str,any]]:
        return [asignatura for asignatura in self.asignaturas if asignatura.get('anio') == anio]
        
    