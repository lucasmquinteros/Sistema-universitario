import pyodbc
from typing import Dict, List, Any, Optional, Tuple, Union
import logging

class DatabaseManager:
    """Gestor de conexiones y operaciones con la base de datos SQL Server"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.logger = logging.getLogger(__name__)
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        try:
            return pyodbc.connect(self.connection_string)
        except pyodbc.Error as e:
            self.logger.error(f"Error al conectar a la base de datos: {str(e)}")
            raise
    
    def execute_stored_procedure(self, sp_name: str, params: tuple = None) -> Union[List[Dict[str, Any]], List[List[Dict[str, Any]]], None]:
        """
        Ejecuta un stored procedure y devuelve los resultados
        
        Args:
            sp_name: Nombre del stored procedure
            params: Tupla de parámetros para el SP
            
        Returns:
            Lista de diccionarios con los resultados o lista de listas si hay múltiples conjuntos
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Construir la llamada al SP
            if params:
                param_placeholders = ','.join(['?' for _ in params])
                cursor.execute(f"EXEC {sp_name} {param_placeholders}", params)
            else:
                cursor.execute(f"EXEC {sp_name}")
                
            # Intentar obtener resultados (puede haber múltiples conjuntos)
            results = []
            while True:
                try:
                    rows = cursor.fetchall()
                    if rows:
                        # Convertir a diccionarios
                        columns = [column[0] for column in cursor.description]
                        result = [dict(zip(columns, row)) for row in rows]
                        results.append(result)
                    
                    # Verificar si hay más resultados
                    if not cursor.nextset():
                        break
                        
                except pyodbc.ProgrammingError:
                    # No hay más resultados o el SP no devuelve resultados
                    break
            
            conn.commit()
            
            # Si solo hay un conjunto de resultados, devolverlo directamente
            if len(results) == 1:
                return results[0]
            elif len(results) > 1:
                return results
            else:
                return None
                
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error al ejecutar SP {sp_name}: {str(e)}")
            raise
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta SQL y devuelve los resultados como diccionarios
        
        Args:
            query: Consulta SQL
            params: Parámetros para la consulta
            
        Returns:
            Lista de diccionarios con los resultados
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            # Convertir resultados a diccionarios
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            conn.commit()
            return results
            
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error al ejecutar consulta: {str(e)}")
            raise
        finally:
            conn.close()