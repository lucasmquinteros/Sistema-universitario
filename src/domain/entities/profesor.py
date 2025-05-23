from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import date

from src.domain.value_objects.nombre_completo import NombreCompleto
from src.domain.value_objects.direccion import Direccion


@dataclass
class Profesor:
    id: Optional[int] = None
    nombre_completo: NombreCompleto = None
    dni: str = ""
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[Direccion] = None
    email: str = ""
    telefono: str = ""
    titulo: str = ""
    especialidad: str = ""
    tipo_contrato: str = ""  # Titular, Adjunto, JTP, etc.
    id_departamento: int = None
    departamento: str = ""
    asignaturas: List[Dict[str, Any]] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea una instancia de Profesor desde un diccionario"""
        profesor = cls(
            id=data.get('Id'),
            dni=data.get('DNI', ''),
            email=data.get('Email', ''),
            telefono=data.get('Telefono', ''),
            titulo=data.get('Titulo', ''),
            especialidad=data.get('Especialidad', ''),
            tipo_contrato=data.get('TipoContrato', ''),
            id_departamento=data.get('Id_Departamento'),
            departamento=data.get('Departamento', '')
        )
        
        # Crear objetos de valor
        if 'Nombre' in data and 'Apellido' in data:
            profesor.nombre_completo = NombreCompleto(
                nombre=data.get('Nombre', ''),
                apellido=data.get('Apellido', '')
            )
            
        if 'FechaNacimiento' in data:
            profesor.fecha_nacimiento = data.get('FechaNacimiento')
            
        if all(k in data for k in ['Calle', 'Numero', 'Ciudad', 'CodigoPostal']):
            profesor.direccion = Direccion(
                calle=data.get('Calle', ''),
                numero=data.get('Numero', ''),
                piso=data.get('Piso'),
                departamento=data.get('Departamento'),
                ciudad=data.get('Ciudad', ''),
                provincia=data.get('Provincia', ''),
                codigo_postal=data.get('CodigoPostal', '')
            )
            
        return profesor
    
    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario"""
        result = {
            'Id': self.id,
            'DNI': self.dni,
            'Email': self.email,
            'Telefono': self.telefono,
            'Titulo': self.titulo,
            'Especialidad': self.especialidad,
            'TipoContrato': self.tipo_contrato,
            'Id_Departamento': self.id_departamento,
            'Departamento': self.departamento
        }
        
        if self.nombre_completo:
            result.update({
                'Nombre': self.nombre_completo.nombre,
                'Apellido': self.nombre_completo.apellido
            })
            
        if self.fecha_nacimiento:
            result['FechaNacimiento'] = self.fecha_nacimiento
            
        if self.direccion:
            result.update({
                'Calle': self.direccion.calle,
                'Numero': self.direccion.numero,
                'Piso': self.direccion.piso,
                'Departamento': self.direccion.departamento,
                'Ciudad': self.direccion.ciudad,
                'Provincia': self.direccion.provincia,
                'CodigoPostal': self.direccion.codigo_postal
            })
            
        return result
    
    def __str__(self):
        if self.nombre_completo:
            return f"{self.nombre_completo} ({self.tipo_contrato})"
        return f"Profesor ID: {self.id}"
