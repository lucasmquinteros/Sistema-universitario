import pyodbc
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

class DatabaseManager:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        
    def get_connection(self):
        return pyodbc.connect(self.connection_string)
    
    def execute_stored_procedure(self, sp_name: str, params: tuple = None):
        """Ejecuta un stored procedure y devuelve los resultados"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            if params:
                cursor.execute(f"EXEC {sp_name} {','.join(['?' for _ in params])}", params)
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
            raise e
        finally:
            conn.close()