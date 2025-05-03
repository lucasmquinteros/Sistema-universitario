# sistema_universitario/services/usuario_service.py
from typing import Dict, List, Any, Optional, Tuple
import hashlib
import os
from .base_service import BaseService
from ..utils.logger import Logger

class UsuarioService(BaseService):
    """Servicio para gestionar usuarios y autenticación"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.logger = Logger.get_instance()
    
    def _hash_password(self, password: str) -> str:
        """
        Genera un hash seguro para la contraseña
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash de la contraseña
        """
        # Generar un salt aleatorio
        salt = os.urandom(32)
        
        # Generar el hash usando PBKDF2
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        
        # Combinar salt y hash para almacenamiento
        return salt.hex() + ':' + key.hex()
    
    def _verify_password(self, stored_password: str, provided_password: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash almacenado
        
        Args:
            stored_password: Hash almacenado
            provided_password: Contraseña proporcionada
            
        Returns:
            True si la contraseña es correcta, False en caso contrario
        """
        # Separar salt y hash
        salt_hex, key_hex = stored_password.split(':')
        salt = bytes.fromhex(salt_hex)
        key = bytes.fromhex(key_hex)
        
        # Generar hash con la contraseña proporcionada
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt,
            100000
        )
        
        # Comparar hashes
        return key == new_key
    
    def crear(self, datos: Dict[str, Any]) -> Optional[int]:
        """
        Crea un nuevo usuario
        
        Args:
            datos: Diccionario con los datos del usuario
            
        Returns:
            ID del usuario creado o None si hubo error
        """
        try:
            # Generar hash de la contraseña
            password_hash = self._hash_password(datos['password'])
            
            # Preparar parámetros para el SP
            params = (
                datos['username'],
                password_hash,
                datos['email'],
                datos['nombre'],
                datos['apellido'],
                datos.get('fecha_creacion'),
                datos.get('activo', True)
            )
            
            # Ejecutar SP con parámetro de salida
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DECLARE @UsuarioId INT;
                EXEC sp_CrearUsuario ?, ?, ?, ?, ?, ?, ?, @UsuarioId OUTPUT;
                SELECT @UsuarioId AS Id;
            """, params)
            
            # Obtener el ID generado
            row = cursor.fetchone()
            usuario_id = row.Id if row else None
            
            conn.commit()
            conn.close()
            
            # Registrar la operación
            self.logger.log_db_operation("CREATE", "Usuario", usuario_id)
            
            return usuario_id
            
        except Exception as e:
            self.logger.error(f"Error al crear usuario: {str(e)}")
            return None
    
    def autenticar(self, username: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Autentica un usuario
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            Tupla (éxito, datos_usuario)
        """
        try:
            # Primero obtener el hash almacenado
            query = "SELECT Id, Username, Password FROM Usuario WHERE Username = ? AND Activo = 1"
            resultados = self.db.execute_query(query, (username,))
            
            if not resultados:
                self.logger.warning(f"Intento de autenticación fallido: usuario {username} no encontrado")
                return False, None
                
            usuario = resultados[0]
            
            # Verificar contraseña
            if not self._verify_password(usuario['Password'], password):
                self.logger.warning(f"Intento de autenticación fallido: contraseña incorrecta para {username}")
                return False, None
                
            # Si la contraseña es correcta, obtener datos completos
            resultados = self.db.execute_stored_procedure("sp_AutenticarUsuario", (username, usuario['Password']))
            
            if not resultados or not resultados[0]:
                return False, None
                
            # Datos del usuario
            datos_usuario = resultados[0][0]
            
            # Agregar roles y permisos
            if len(resultados) > 1:
                datos_usuario['roles'] = resultados[1]
                
            if len(resultados) > 2:
                datos_usuario['permisos'] = resultados[2]
                
            self.logger.info(f"Usuario {username} autenticado correctamente")
            return True, datos_usuario
            
        except Exception as e:
            self.logger.error(f"Error al autenticar usuario: {str(e)}")
            return False, None
    
    def verificar_permiso(self, usuario_id: int, codigo_permiso: str) -> bool:
        """
        Verifica si un usuario tiene un permiso específico
        
        Args:
            usuario_id: ID del usuario
            codigo_permiso: Código del permiso a verificar
            
        Returns:
            True si el usuario tiene el permiso, False en caso contrario
        """
        try:
            query = """
                SELECT 1
                FROM Permiso p
                JOIN RolxPermiso rp ON p.Id = rp.Id_Permiso
                JOIN UsuarioxRol ur ON rp.Id_Rol = ur.Id_Rol
                WHERE ur.Id_Usuario = ? AND p.Codigo = ?
            """
            resultados = self.db.execute_query(query, (usuario_id, codigo_permiso))
            
            return len(resultados) > 0
            
        except Exception as e:
            self.logger.error(f"Error al verificar permiso: {str(e)}")
            return False