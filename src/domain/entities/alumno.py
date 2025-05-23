from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date

from src.domain.value_objects.nombre_completo import NombreCompleto
from src.domain.value_objects.direccion import Direccion


@dataclass
class Alumno:
    id: Optional[int] = None
    nombre_completo: NombreCompleto = None
    dni: str = ""
    fecha_nacimiento: date = None
    direccion: Direccion = None
    email: str = ""
    telefono: str = ""
    legajo: str = ""
    fecha_ingreso: date = None
    estado: str = "Activo"  # Activo, Inactivo, Graduado, etc.

    @classmethod
    def from_dict(cls, data: dict):
        """Crea una instancia de Alumno desde un diccionario"""
        alumno = cls(
            id=data.get("Id"),
            dni=data.get("DNI", ""),
            email=data.get("Email", ""),
            telefono=data.get("Telefono", ""),
            legajo=data.get("Legajo", ""),
            estado=data.get("Estado", "Activo"),
        )

        # Crear objetos de valor
        if "Nombre" in data and "Apellido" in data:
            alumno.nombre_completo = NombreCompleto(
                nombre=data.get("Nombre", ""), apellido=data.get("Apellido", "")
            )

        if "FechaNacimiento" in data:
            alumno.fecha_nacimiento = data.get("FechaNacimiento")

        if "FechaIngreso" in data:
            alumno.fecha_ingreso = data.get("FechaIngreso")

        if all(k in data for k in ["Calle", "Numero", "Ciudad", "CodigoPostal"]):
            alumno.direccion = Direccion(
                calle=data.get("Calle", ""),
                numero=data.get("Numero", ""),
                piso=data.get("Piso"),
                departamento=data.get("Departamento"),
                ciudad=data.get("Ciudad", ""),
                provincia=data.get("Provincia", ""),
                codigo_postal=data.get("CodigoPostal", ""),
            )

        return alumno

    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario"""
        result = {
            "Id": self.id,
            "DNI": self.dni,
            "Email": self.email,
            "Telefono": self.telefono,
            "Legajo": self.legajo,
            "Estado": self.estado,
        }

        if self.nombre_completo:
            result.update(
                {
                    "Nombre": self.nombre_completo.nombre,
                    "Apellido": self.nombre_completo.apellido,
                }
            )

        if self.fecha_nacimiento:
            result["FechaNacimiento"] = self.fecha_nacimiento

        if self.fecha_ingreso:
            result["FechaIngreso"] = self.fecha_ingreso

        if self.direccion:
            result.update(
                {
                    "Calle": self.direccion.calle,
                    "Numero": self.direccion.numero,
                    "Piso": self.direccion.piso,
                    "Departamento": self.direccion.departamento,
                    "Ciudad": self.direccion.ciudad,
                    "Provincia": self.direccion.provincia,
                    "CodigoPostal": self.direccion.codigo_postal,
                }
            )

        return result

    def __str__(self):
        if self.nombre_completo:
            return f"{self.nombre_completo} (Legajo: {self.legajo})"
        return f"Alumno ID: {self.id} (Legajo: {self.legajo})"
