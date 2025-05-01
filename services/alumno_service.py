from typing import Dict, List, Any, Optional
from datetime import datetime

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
            cursor.execute("""
                DECLARE @AlumnoId INT;
                EXEC sp_CrearAlumno ?, ?, ?, ?, ?, ?, ?, ?, ?, @AlumnoId OUTPUT;
                SELECT @AlumnoId AS Id;
            """, params)
            
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
    
    def _crear_usuario_alumno(self, alumno_id: int, datos: Dict[str, Any]) -> bool:
        """Método auxiliar para crear usuario asociado a un alumno"""
        try:
            # Aquí podrías llamar a otro SP para crear el usuario
            # O usar la clase UsuarioService
            return True
        except Exception:
            return False