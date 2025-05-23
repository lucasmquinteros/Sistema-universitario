from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class ProfesorDTO:
    """DTO para transferir datos de Profesor entre capas"""

    id: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    dni: str = ""
    fecha_nacimiento: Optional[datetime] = None
    email: str = ""
    telefono: str = ""
    direccion: str = ""
    fecha_ingreso: Optional[datetime] = None
    departamento_id: Optional[int] = None
    departamento_nombre: Optional[str] = None
    titulo: str = ""
    especialidad: str = ""
    estado: str = "Activo"

    @classmethod
    def from_entity(cls, profesor) -> "ProfesorDTO":
        """Crea un DTO a partir de una entidad Profesor"""
        return cls(
            id=profesor.id,
            nombre=profesor.nombre,
            apellido=profesor.apellido,
            dni=profesor.dni,
            fecha_nacimiento=profesor.fecha_nacimiento,
            email=profesor.email,
            telefono=profesor.telefono,
            direccion=profesor.direccion,
            fecha_ingreso=profesor.fecha_ingreso,
            departamento_id=profesor.departamento_id,
            titulo=profesor.titulo,
            especialidad=profesor.especialidad,
            estado=profesor.estado,
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
            "departamento_id": self.departamento_id,
            "departamento_nombre": self.departamento_nombre,
            "titulo": self.titulo,
            "especialidad": self.especialidad,
            "estado": self.estado,
        }


@dataclass
class ProfesorDetalleDTO(ProfesorDTO):
    """DTO con información detallada de un Profesor, incluyendo asignaturas"""

    asignaturas: List[dict] = None

    @classmethod
    def from_entity_with_asignaturas(
        cls, profesor, asignaturas: List[dict]
    ) -> "ProfesorDetalleDTO":
        """Crea un DTO detallado a partir de una entidad Profesor y sus asignaturas"""
        dto = cls.from_entity(profesor)
        dto.asignaturas = asignaturas
        return dto
