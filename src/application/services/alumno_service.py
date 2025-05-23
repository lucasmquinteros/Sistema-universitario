from typing import List, Optional, Tuple, Dict, Any
from ...domain.repositories.alumno_repository import AlumnoRepository
from ...domain.entities.alumno import Alumno
from ..dtos.alumno_dto import AlumnoDTO, AlumnoDetalleDTO

class AlumnoService:
    """Servicio de aplicación para gestionar alumnos"""
    
    def __init__(self, alumno_repository: AlumnoRepository):
        self.alumno_repository = alumno_repository
    
    def obtener_alumno(self, alumno_id: int) -> Optional[AlumnoDTO]:
        """
        Obtiene un alumno por su ID
        
        Args:
            alumno_id: ID del alumno
            
        Returns:
            DTO del alumno o None si no existe
        """
        alumno = self.alumno_repository.obtener_por_id(alumno_id)
        if not alumno:
            return None
        return AlumnoDTO.from_entity(alumno)
    
    def obtener_alumno_detalle(self, alumno_id: int) -> Optional[AlumnoDetalleDTO]:
        """
        Obtiene un alumno con detalle de cursadas por su ID
        
        Args:
            alumno_id: ID del alumno
            
        Returns:
            DTO detallado del alumno o None si no existe
        """
        alumno = self.alumno_repository.obtener_por_id(alumno_id)
        if not alumno:
            return None
        
        cursadas = self.alumno_repository.obtener_historial_academico(alumno_id)
        return AlumnoDetalleDTO.from_entity_with_cursadas(alumno, cursadas)
    
    def obtener_todos_alumnos(self) -> List[AlumnoDTO]:
        """
        Obtiene todos los alumnos
        
        Returns:
            Lista de DTOs de alumnos
        """
        alumnos = self.alumno_repository.obtener_todos()
        return [AlumnoDTO.from_entity(alumno) for alumno in alumnos]
    
    def crear_alumno(self, alumno_dto: AlumnoDTO) -> Tuple[bool, Optional[AlumnoDTO], Optional[str]]:
        """
        Crea un nuevo alumno
        
        Args:
            alumno_dto: DTO con los datos del alumno a crear
            
        Returns:
            Tupla con (éxito, DTO del alumno creado, mensaje)
        """
        # Validar datos
        if not alumno_dto.dni or not alumno_dto.nombre or not alumno_dto.apellido:
            return False, None, "Los campos DNI, nombre y apellido son obligatorios"
        
        # Verificar si ya existe un alumno con el mismo DNI
        alumno_existente = self.alumno_repository.obtener_por_dni(alumno_dto.dni)
        if alumno_existente:
            return False, None, f"Ya existe un alumno con DNI {alumno_dto.dni}"
        
        # Crear entidad desde DTO
        alumno = Alumno(
            nombre=alumno_dto.nombre,
            apellido=alumno_dto.apellido,
            dni=alumno_dto.dni,
            fecha_nacimiento=alumno_dto.fecha_nacimiento,
            email=alumno_dto.email,
            telefono=alumno_dto.telefono,
            direccion=alumno_dto.direccion,
            fecha_ingreso=alumno_dto.fecha_ingreso,
            carrera_id=alumno_dto.carrera_id,
            legajo=alumno_dto.legajo,
            estado=alumno_dto.estado
        )
        
        # Guardar en repositorio
        alumno_creado = self.alumno_repository.crear(alumno)
        
        return True, AlumnoDTO.from_entity(alumno_creado), "Alumno creado con éxito"
    
    def actualizar_alumno(self, alumno_id: int, alumno_dto: AlumnoDTO) -> Tuple[bool, Optional[AlumnoDTO], Optional[str]]:
        """
        Actualiza un alumno existente
        
        Args:
            alumno_id: ID del alumno a actualizar
            alumno_dto: DTO con los datos actualizados
            
        Returns:
            Tupla con (éxito, DTO del alumno actualizado, mensaje)
        """
        # Verificar que el alumno existe
        alumno_existente = self.alumno_repository.obtener_por_id(alumno_id)
        if not alumno_existente:
            return False, None, f"No existe un alumno con ID {alumno_id}"
        
        # Actualizar entidad
        alumno_existente.nombre = alumno_dto.nombre
        alumno_existente.apellido = alumno_dto.apellido
        alumno_existente.email = alumno_dto.email
        alumno_existente.telefono = alumno_dto.telefono
        alumno_existente.direccion = alumno_dto.direccion
        alumno_existente.carrera_id = alumno_dto.carrera_id
        alumno_existente.estado = alumno_dto.estado
        
        # Guardar en repositorio
        alumno_actualizado = self.alumno_repository.actualizar(alumno_existente)
        
        return True, AlumnoDTO.from_entity(alumno_actualizado), "Alumno actualizado con éxito"
    
    def eliminar_alumno(self, alumno_id: int) -> Tuple[bool, Optional[str]]:
        """
        Elimina un alumno
        
        Args:
            alumno_id: ID del alumno a eliminar
            
        Returns