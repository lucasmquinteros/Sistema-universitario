from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.alumno import Alumno


class AlumnoRepository(ABC):
    @abstractmethod
    def get_by_id(self, alumno_id: int) -> Optional[Alumno]:
        """Obtiene un alumno por su ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[Alumno]:
        """Obtiene todos los alumnos"""
        pass

    @abstractmethod
    def get_by_legajo(self, legajo: str) -> Optional[Alumno]:
        """Obtiene un alumno por su legajo"""
        pass

    @abstractmethod
    def save(self, alumno: Alumno) -> int:
        """Guarda un alumno y devuelve su ID"""
        pass

    @abstractmethod
    def update(self, alumno: Alumno) -> bool:
        """Actualiza un alumno existente"""
        pass

    @abstractmethod
    def delete(self, alumno_id: int) -> bool:
        """Elimina un alumno por su ID"""
        pass

    @abstractmethod
    def get_by_filter(self, **kwargs) -> List[Alumno]:
        """Obtiene alumnos que coincidan con los filtros especificados"""
        pass
