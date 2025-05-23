from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class AlumnoDTO:
    """DTO para transferir datos de Alumno entre capas"""

    id: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    dni: str = ""
    fecha_nacimiento: Optional[datetime] = None
    email: str = ""
    telefono: str = ""
    direccion: str = ""
    fecha_ingreso: Optional[datetime] = None
    carrera_id: Optional[int] = None
    carrera_nombre: Optional[str] = None
    legajo: str = ""
    estado: str = "Activo"

    @classmethod
    def from_entity(cls, alumno) -> "AlumnoDTO":
        """Crea un DTO a partir de una entidad Alumno"""
        return cls(
            id=alumno.id,
            nombre=alumno.nombre,
            apellido=alumno.apellido,
            dni=alumno.dni,
            fecha_nacimiento=alumno.fecha_nacimiento,
            email=alumno.email,
            telefono=alumno.telefono,
            direccion=alumno.direccion,
            fecha_ingreso=alumno.fecha_ingreso,
            carrera_id=alumno.carrera_id,
            legajo=alumno.legajo,
            estado=alumno.estado,
        )

    def to_dict(self) -> dict:
        """Convierte el DTO a un diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat()
            if self.fecha_nacimiento
            else None,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "fecha_ingreso": self.fecha_ingreso.isoformat()
            if self.fecha_ingreso
            else None,
            "carrera_id": self.carrera_id,
            "carrera_nombre": self.carrera_nombre,
            "legajo": self.legajo,
            "estado": self.estado,
        }


@dataclass
class AlumnoDetalleDTO(AlumnoDTO):
    """DTO con información detallada de un Alumno, incluyendo cursadas"""

    cursadas: List[dict] = None

    @classmethod
    def from_entity_with_cursadas(
        cls, alumno, cursadas: List[dict]
    ) -> "AlumnoDetalleDTO":
        """Crea un DTO detallado a partir de una entidad Alumno y sus cursadas"""
        dto = cls.from_entity(alumno)
        dto.cursadas = cursadas
        return dto
