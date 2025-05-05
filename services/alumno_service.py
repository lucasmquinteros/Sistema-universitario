from typing import Dict, List, Any, Optional
from datetime import datetime
from models.alumno import Alumno
from models.usuario import Usuario
from db.manager import DatabaseManager

class AlumnoService:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def crear(self, datos: Dict[str, Any]) -> Optional[int]:
        """Alta de un nuevo alumno usando stored procedure"""
        try:
            # Preparar parámetros para el SP
            params = (
                datos['nombre'],
                datos['apellido'],
                datos['dni'],
                datos['fecha_nacimiento'],
                datos['email'],
                datos.get('telefono'),
                datos.get('direccion'),
                datos.get('fecha_ingreso'),
                datos.get('carrera_id')
            )
            
            # Ejecutar SP con parámetro de salida
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # SQL Server permite parámetros de salida
            cursor = self.db.execute_stored_procedure("sp_CrearAlumno", params, output=True)
            # Obtener el ID generado
            row = cursor.fetchone()
            alumno_id = row.Id if row else None
            
            conn.commit()
            
            # Si se proporcionan datos de usuario, crear usuario
            if alumno_id and 'usuario' in datos:
                self._crear_usuario_alumno(alumno_id, datos)
                
            return alumno_id
            
        except Exception as e:
            # Loguear el error
            print(f"Error al crear alumno: {str(e)}")
            return None
    
    def obtener(self, alumno_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un alumno por ID usando stored procedure"""
        try:
            # Ejecutar SP
            resultados = self.db.execute_stored_procedure("sp_ObtenerAlumno", (alumno_id,))
            
            if not resultados or len(resultados) < 1 or not resultados[0]:
                return None
                
            # El SP devuelve múltiples conjuntos de resultados
            # resultados[0] = datos básicos del alumno
            # resultados[1] = carreras
            # resultados[2] = cursadas actuales
            # resultados[3] = usuario asociado
            
            alumno = resultados[0][0]  # Primer registro del primer conjunto
            
            # Agregar información adicional
            if len(resultados) > 1:
                alumno['carreras'] = resultados[1]
            
            if len(resultados) > 2:
                alumno['cursadas_actuales'] = resultados[2]
                
            if len(resultados) > 3 and resultados[3]:
                alumno['usuario'] = resultados[3][0]
                
            return alumno
            
        except Exception as e:
            print(f"Error al obtener alumno: {str(e)}")
            return None
    
    def modificar(self, alumno_id: int, datos: Dict[str, Any]) -> bool:
        """Modifica un alumno usando stored procedure"""
        try:
            # Preparar parámetros para el SP
            params = [alumno_id]
            
            # Agregar parámetros opcionales
            for campo in ['nombre', 'apellido', 'email', 'telefono', 'direccion', 'estado']:
                params.append(datos.get(campo))
                
            # Ejecutar SP
            self.db.execute_stored_procedure("sp_ModificarAlumno", tuple(params))
            return True
            
        except Exception as e:
            print(f"Error al modificar alumno: {str(e)}")
            return False
    
    def listarAlumnos(self, filtros: Dict[str, Any]) -> List[Dict[Alumno, Any]]:
        """Lista alumnos aplicando filtros usando stored procedure"""
        try:
            # Preparar parámetros para el SP
            params = (
                filtros.get('Carrera_id'),
                filtros.get('PlanEstudioId'),
                filtros.get('CursadaId'),
                filtros.get('Estado'),
                filtros.get('Legajo')
            )
            
            # Ejecutar SP
            resultados = self.db.execute_stored_procedure("sp_ListarAlumnos", params)
            
            return [dict(row) for row in resultados] if resultados else []
            
        except Exception as e:
            print(f"Error al listar alumnos: {str(e)}")
            return []
        
    def eliminar(self, alumno_id: int, Dni: str) -> bool:
        """Elimina un alumno usando stored procedure"""
        try:
            # Ejecutar SP
            self.db.execute_stored_procedure("sp_EliminarAlumno", (alumno_id, Dni))
            return True
            
        except Exception as e:
            print(f"Error al eliminar alumno: {str(e)}")
            return False
        
    def inscribirAlumnoEnCarrera(self, alumno_id: int, carrera_id: int) -> bool:
        """Inscribe un alumno en una carrera usando stored procedure"""
        try:
            # Ejecutar SP
            self.db.execute_stored_procedure("sp_InscribirAlumnoCarrera", (alumno_id, carrera_id))
            return True
            
        except Exception as e:
            print(f"Error al inscribir alumno en carrera: {str(e)}")
            return False
    
    def inscribirAlumnoEnAsignatura(self, alumno_id: int, asignatura_id: int) -> bool:
        """Inscribe un alumno en una asignatura usando stored procedure"""
        try:
            # Ejecutar SP
            self.db.execute_stored_procedure("sp_InscribirAlumnoAsignatura", (alumno_id, asignatura_id))
            return True
            
        except Exception as e:
            print(f"Error al inscribir alumno en asignatura: {str(e)}")
            return False
        
    def registrarNota(self, alumno_id: int, asignatura_id: int, nota: float) -> bool:
        """Registra una nota para un alumno en una asignatura usando stored procedure"""
        try:
            # Ejecutar SP
            self.db.execute_stored_procedure("sp_RegistrarNota", (alumno_id, asignatura_id, nota))
            return True
            
        except Exception as e:
            print(f"Error al registrar nota: {str(e)}")
            return False
        
    def obtenerHistorialAcademico(self, alumno_id: int) -> Optional[List[Dict[str, Any]]]:
        """Obtiene el historial académico de un alumno usando stored procedure"""
        try:
            # Ejecutar SP
            resultados = self.db.execute_stored_procedure("sp_ObtenerHistorialAcademico", (alumno_id,))
            
            return [dict(row) for row in resultados] if resultados else []
            
        except Exception as e:
            print(f"Error al obtener historial académico: {str(e)}")
            return None
        
    def verificarCorrelativas(self, alumno_id: int, asignatura_id: int) -> bool:
        """Verifica si un alumno cumple con las correlativas de una asignatura usando stored procedure"""
        try:
            # Ejecutar SP
            resultados = self.db.execute_stored_procedure("sp_VerificarCorrelativas", (alumno_id, asignatura_id))
            
            if resultados and len(resultados) > 0:
                return resultados[0][0] == 1  # Retorna True si cumple con las correlativas
            
            return False
            
        except Exception as e:
            print(f"Error al verificar correlativas: {str(e)}")
            return False