from typing import Optional, Tuple, List
from ..entities.alumno import Alumno
from ..repositories.alumno_repository import AlumnoRepository


class InscripcionService:
    """Servicio de dominio para gestionar inscripciones de alumnos a asignaturas"""

    def __init__(self, alumno_repository: AlumnoRepository):
        self.alumno_repository = alumno_repository

    def inscribir_alumno_asignatura(
        self, alumno_id: int, asignatura_id: int, año_academico: int, cuatrimestre: int
    ) -> Tuple[bool, Optional[str]]:
        """
        Inscribe un alumno a una asignatura

        Args:
            alumno_id: ID del alumno
            asignatura_id: ID de la asignatura
            año_academico: Año académico de la inscripción
            cuatrimestre: Cuatrimestre de la inscripción

        Returns:
            Tupla con (éxito, mensaje)
        """
        # Verificar que el alumno existe
        alumno = self.alumno_repository.obtener_por_id(alumno_id)
        if not alumno:
            return False, "El alumno no existe"

        # Verificar que el alumno esté activo
        if alumno.estado != "Activo":
            return False, f"El alumno no está activo. Estado actual: {alumno.estado}"

        # Aquí iría la lógica para verificar correlativas, cupos, etc.
        # ...

        # Lógica para inscribir al alumno
        # Esta implementación dependerá de cómo se manejen las inscripciones en el sistema

        return True, "Inscripción realizada con éxito"

    def verificar_correlativas(
        self, alumno_id: int, asignatura_id: int
    ) -> Tuple[bool, Optional[str]]:
        """
        Verifica si un alumno cumple con las correlativas para una asignatura

        Args:
            alumno_id: ID del alumno
            asignatura_id: ID de la asignatura

        Returns:
            Tupla con (cumple_correlativas, mensaje)
        """
        # Implementación de la lógica para verificar correlativas
        # ...

        return True, "El alumno cumple con todas las correlativas"
