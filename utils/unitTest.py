# sistema_universitario/examples/utils_example.py
from utils.validators import Validator
from utils.security_manager import SecurityManager
from utils.config_manager import ConfigManager
from utils.logger import Logger

def ejemplo_validator():
    print("=== Ejemplo de Validator ===")
    
    # Validar un correo electrónico
    email = "usuario@universidad.edu"
    valido, mensaje = Validator.validate_email(email)
    print(f"Email '{email}': {'Válido' if valido else 'Inválido'} - {mensaje or ''}")
    
    # Validar un correo inválido
    email_invalido = "usuario@"
    valido, mensaje = Validator.validate_email(email_invalido)
    print(f"Email '{email_invalido}': {'Válido' if valido else 'Inválido'} - {mensaje or ''}")
    
    # Validar un DNI
    dni = "30.123.456"
    valido, mensaje = Validator.validate_dni(dni)
    print(f"DNI '{dni}': {'Válido' if valido else 'Inválido'} - {mensaje or ''}")
    
    # Validar un modelo completo
    datos_alumno = {
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'dni': '30123456',
        'email': 'juan.perez@universidad.edu',
        'fecha_nacimiento': '1990-05-15'
    }
    
    reglas_validacion = {
        'nombre': {'type': 'string', 'min_length': 2, 'max_length': 50, 'required': True},
        'apellido': {'type': 'string', 'min_length': 2, 'max_length': 50, 'required': True},
        'dni': {'type': 'dni', 'required': True},
        'email': {'type': 'email', 'required': True},
        'fecha_nacimiento': {'type': 'date', 'required': True}
    }
    
    errores = Validator.validate_model(datos_alumno, reglas_validacion)
    
    if errores:
        print("Errores de validación:")
        for campo, error in errores.items():
            print(f"  - {campo}: {error}")
    else:
        print("Modelo válido")

def ejemplo_security_manager():
    print("\n=== Ejemplo de SecurityManager ===")
    
    # Obtener instancia
    security = SecurityManager.get_instance()
    
    # Hash de contraseña
    password = "Contraseña123!"
    hash_password = security.hash_password(password)
    print(f"Contraseña: {password}")
    print(f"Hash: {hash_password}")
    
    # Verificar contraseña
    verificacion = security.verify_password(hash_password, password)
    print(f"Verificación correcta: {verificacion}")
    
    verificacion_incorrecta = security.verify_password(hash_password, "ContraseñaIncorrecta")
    print(f"Verificación incorrecta: {verificacion_incorrecta}")
    
    # Generar token
    token = security.generate_token(user_id=123)
    print(f"Token generado: {token}")
    
    # Validar token
    validacion = security.validate_token(token)
    print(f"Validación de token: {validacion}")
    
    # Cifrar datos
    datos = "Información sensible"
    datos_cifrados = security.encrypt_data(datos)
    print(f"Datos cifrados: {datos_cifrados}")
    
    # Descifrar datos
    datos_descifrados = security.decrypt_data(datos_cifrados)
    print(f"Datos descifrados: {datos_descifrados}")

def ejemplo_config_manager():
    print("\n=== Ejemplo de ConfigManager ===")
    
    # Obtener instancia
    config = ConfigManager.get_instance()
    
    # Obtener valores de configuración
    db_server = config.get('database.server', 'localhost')
    print(f"Servidor de base de datos: {db_server}")
    
    log_level = config.get('logging.level', 'INFO')
    print(f"Nivel de logging: {log_level}")
    
    # Establecer valores de configuración
    config.set('app.debug', False)
    print(f"Modo debug: {config.get('app.debug')}")
    
    # Guardar configuración
    guardado = config.save_config()
    print(f"Configuración guardada: {guardado}")

def ejemplo_logger():
    print("\n=== Ejemplo de Logger ===")
    
    # Obtener instancia
    logger = Logger.get_instance()
    
    # Registrar mensajes
    logger.info("Aplicación iniciada")
    logger.warning("Advertencia: conexión lenta")
    
    try:
        # Provocar un error
        resultado = 10 / 0
    except Exception as e:
        logger.error(f"Error en la operación: {str(e)}")
    
    # Registrar operación en base de datos
    logger.log_db_operation("CREATE", "Alumno", 123, 1, "Creación de alumno")
    
    print("Mensajes registrados en el log")

if __name__ == "__main__":
    ejemplo_validator()
    ejemplo_security_manager()
    ejemplo_config_manager()
    ejemplo_logger()