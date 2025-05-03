# sistema_universitario/utils/security_manager.py
import hashlib
import os
import base64
import hmac
import json
import time
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecurityManager:
    """
    Clase para gestionar aspectos de seguridad del sistema
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls, secret_key: Optional[str] = None):
        """Implementación de Singleton para el SecurityManager"""
        if cls._instance is None:
            cls._instance = cls(secret_key)
        return cls._instance
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Inicializa el gestor de seguridad
        
        Args:
            secret_key: Clave secreta para operaciones criptográficas
        """
        # Si no se proporciona una clave secreta, usar una predeterminada (¡no recomendado en producción!)
        self.secret_key = secret_key or "sistema_universitario_secret_key_change_in_production"
        
        # Derivar una clave para cifrado simétrico
        salt = b'sistema_universitario_salt'  # En producción, esto debería ser aleatorio y almacenado
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.secret_key.encode()))
        self.cipher_suite = Fernet(key)
    
    def hash_password(self, password: str) -> str:
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
    
    def verify_password(self, stored_password: str, provided_password: str) -> bool:
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
    
    def generate_token(self, user_id: int, expiry: int = 3600) -> str:
        """
        Genera un token JWT para autenticación
        
        Args:
            user_id: ID del usuario
            expiry: Tiempo de expiración en segundos (por defecto 1 hora)
            
        Returns:
            Token JWT
        """
        # Crear payload
        payload = {
            'user_id': user_id,
            'exp': int(time.time()) + expiry,
            'iat': int(time.time())
        }
        
        # Codificar header y payload
        header = {'alg': 'HS256', 'typ': 'JWT'}
        header_json = json.dumps(header, separators=(',', ':')).encode()
        header_b64 = base64.urlsafe_b64encode(header_json).decode().rstrip('=')
        
        payload_json = json.dumps(payload, separators=(',', ':')).encode()
        payload_b64 = base64.urlsafe_b64encode(payload_json).decode().rstrip('=')
        
        # Crear firma
        to_sign = f"{header_b64}.{payload_b64}".encode()
        signature = hmac.new(
            self.secret_key.encode(),
            to_sign,
            hashlib.sha256
        ).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
        
        # Combinar para formar el token
        return f"{header_b64}.{payload_b64}.{signature_b64}"
    
    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Valida un token JWT
        
        Args:
            token: Token JWT a validar
            
        Returns:
            Payload del token si es válido, o diccionario con error
        """
        try:
            # Separar partes del token
            header_b64, payload_b64, signature_b64 = token.split('.')
            
            # Verificar firma
            to_verify = f"{header_b64}.{payload_b64}".encode()
            signature = base64.urlsafe_b64decode(signature_b64 + '=' * (4 - len(signature_b64) % 4))
            
            expected_signature = hmac.new(
                self.secret_key.encode(),
                to_verify,
                hashlib.sha256
            ).digest()
            
            if not hmac.compare_digest(signature, expected_signature):
                return {'error': 'Firma inválida'}
            
            # Decodificar payload
            payload_json = base64.urlsafe_b64decode(payload_b64 + '=' * (4 - len(payload_b64) % 4))
            payload = json.loads(payload_json)
            
            # Verificar expiración
            if payload.get('exp', 0) < int(time.time()):
                return {'error': 'Token expirado'}
                
            return payload
            
        except Exception as e:
            return {'error': f'Error al validar token: {str(e)}'}
    
    def encrypt_data(self, data: str) -> str:
        """
        Cifra datos sensibles
        
        Args:
            data: Datos a cifrar
            
        Returns:
            Datos cifrados en formato base64
        """
        return self.cipher_suite.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Descifra datos sensibles
        
        Args:
            encrypted_data: Datos cifrados en formato base64
            
        Returns:
            Datos descifrados
        """
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()