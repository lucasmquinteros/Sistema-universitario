# sistema_universitario/api/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import date

# Esquemas para Profesor
class ProfesorBase(BaseModel):
    nombre: str
    apellido: str
    dni: str
    email: EmailStr
    telefono: Optional[str] = None
    titulo: str
    especialidad: Optional[str] = None
    tipo_contrato: str
    id_departamento: int

class ProfesorCreate(ProfesorBase):
    fecha_ingreso: Optional[date] = None

class AsignaturaInfo(BaseModel):
    id: int
    nombre: str
    rol: Optional[str] = None
    año_academico: Optional[int] = None
    cuatrimestre: Optional[int] = None

class ProfesorResponse(ProfesorBase):
    id: int
    fecha_ingreso: Optional[date] = None
    departamento: Optional[str] = None
    asignaturas: List[AsignaturaInfo] = []
    
    class Config:
        orm_mode = True

class ProfesorList(BaseModel):
    id: int
    nombre: str
    apellido: str
    titulo: str
    especialidad: Optional[str] = None
    departamento: Optional[str] = None
    
    class Config:
        orm_mode = True

# Esquemas para Alumno
class AlumnoBase(BaseModel):
    nombre: str
    apellido: str
    dni: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[date] = None

class AlumnoCreate(AlumnoBase):
    fecha_ingreso: Optional[date] = None
    carrera_id: Optional[int] = None

class CarreraInfo(BaseModel):
    id: int
    nombre: str
    fecha_inscripcion: Optional[date] = None

class AlumnoResponse(AlumnoBase):
    id: int
    fecha_ingreso: date
    estado: Optional[str] = None
    carreras: List[CarreraInfo] = []
    
    class Config:
        orm_mode = True

class AlumnoList(BaseModel):
    id: int
    nombre: str
    apellido: str
    dni: str
    estado: Optional[str] = None
    
    class Config:
        orm_mode = True

# Esquemas para Asignatura
class AsignaturaBase(BaseModel):
    nombre: str
    hsemanal: int
    htotales: int
    creditos: int
    id_area: int
    id_regimen: int
    id_depto: int

class AsignaturaCreate(AsignaturaBase):
    pass

class AsignaturaResponse(AsignaturaBase):
    id: int
    area: Optional[str] = None
    regimen: Optional[str] = None
    departamento: Optional[str] = None
    
    class Config:
        orm_mode = True