# sistema_universitario/utils/validator.py
import re
from datetime import date, datetime
from typing import Dict, Any, Optional, List, Union

class Validator:
    """
    Clase para validar datos de entrada en el sistema
    """
    
    @staticmethod
    def validate_string(value: Optional[str], min_length: int = 0, max_length: int = None, 
                        required: bool = True) -> tuple:
        """
        Valida una cadena de texto
        
        Args:
            value: Valor a validar
            min_length: Longitud mínima
            max_length: Longitud máxima
            required: Si es requerido
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        # Verificar si es requerido
        if required and (value is None or value.strip() == ""):
            return False, "Este campo es requerido"
            
        # Si no es requerido y está vacío, es válido
        if not required and (value is None or value.strip() == ""):
            return True, None
            
        # Verificar longitud mínima
        if min_length > 0 and len(value) < min_length:
            return False, f"Debe tener al menos {min_length} caracteres"
            
        # Verificar longitud máxima
        if max_length and len(value) > max_length:
            return False, f"No debe exceder {max_length} caracteres"
            
        return True, None
    
    @staticmethod
    def validate_email(email: Optional[str], required: bool = True) -> tuple:
        """
        Valida un correo electrónico
        
        Args:
            email: Correo a validar
            required: Si es requerido
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        # Verificar si es requerido
        if required and (email is None or email.strip() == ""):
            return False, "El correo electrónico es requerido"
            
        # Si no es requerido y está vacío, es válido
        if not required and (email is None or email.strip() == ""):
            return True, None
            
        # Patrón de validación de correo
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False, "El formato del correo electrónico no es válido"
            
        return True, None
    
    @staticmethod
    def validate_number(value: Optional[Union[int, float]], min_value: Optional[Union[int, float]] = None, 
                        max_value: Optional[Union[int, float]] = None, required: bool = True) -> tuple:
        """
        Valida un número
        
        Args:
            value: Valor a validar
            min_value: Valor mínimo
            max_value: Valor máximo
            required: Si es requerido
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        # Verificar si es requerido
        if required and value is None:
            return False, "Este campo es requerido"
            
        # Si no es requerido y está vacío, es válido
        if not required and value is None:
            return True, None
            
        # Verificar valor mínimo
        if min_value is not None and value < min_value:
            return False, f"El valor debe ser mayor o igual a {min_value}"
            
        # Verificar valor máximo
        if max_value is not None and value > max_value:
            return False, f"El valor debe ser menor o igual a {max_value}"
            
        return True, None
    
    @staticmethod
    def validate_date(value: Optional[Union[date, datetime, str]], min_date: Optional[date] = None, 
                      max_date: Optional[date] = None, required: bool = True) -> tuple:
        """
        Valida una fecha
        
        Args:
            value: Fecha a validar
            min_date: Fecha mínima
            max_date: Fecha máxima
            required: Si es requerido
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        # Verificar si es requerido
        if required and value is None:
            return False, "Este campo es requerido"
            
        # Si no es requerido y está vacío, es válido
        if not required and value is None:
            return True, None
            
        # Convertir a objeto date si es string
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                return False, "El formato de fecha debe ser YYYY-MM-DD"
                
        # Convertir a date si es datetime
        if isinstance(value, datetime):
            value = value.date()
            
        # Verificar fecha mínima
        if min_date and value < min_date:
            return False, f"La fecha debe ser posterior a {min_date.strftime('%Y-%m-%d')}"
            
        # Verificar fecha máxima
        if max_date and value > max_date:
            return False, f"La fecha debe ser anterior a {max_date.strftime('%Y-%m-%d')}"
            
        return True, None
    
    @staticmethod
    def validate_dni(dni: Optional[str], required: bool = True) -> tuple:
        """
        Valida un DNI (específico para Argentina)
        
        Args:
            dni: DNI a validar
            required: Si es requerido
            
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        # Verificar si es requerido
        if required and (dni is None or dni.strip() == ""):
            return False, "El DNI es requerido"
            
        # Si no es requerido y está vacío, es válido
        if not required and (dni is None or dni.strip() == ""):
            return True, None
            
        # Eliminar puntos y espacios
        dni_clean = dni.replace(".", "").replace(" ", "")
        
        # Verificar que solo contiene dígitos
        if not dni_clean.isdigit():
            return False, "El DNI debe contener solo números"
            
        # Verificar longitud (7 u 8 dígitos para Argentina)
        if len(dni_clean) < 7 or len(dni_clean) > 8:
            return False, "El DNI debe tener 7 u 8 dígitos"
            
        return True, None
    
    @staticmethod
    def validate_model(model: Dict[str, Any], validation_rules: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """
        Valida un modelo completo según reglas definidas
        
        Args:
            model: Diccionario con los datos del modelo
            validation_rules: Reglas de validación
            
        Returns:
            Diccionario con errores (vacío si no hay errores)
        """
        errors = {}
        
        for field, rules in validation_rules.items():
            value = model.get(field)
            
            # Determinar el tipo de validación
            if rules.get('type') == 'string':
                valid, message = Validator.validate_string(
                    value, 
                    rules.get('min_length', 0), 
                    rules.get('max_length'), 
                    rules.get('required', True)
                )
            elif rules.get('type') == 'email':
                valid, message = Validator.validate_email(
                    value, 
                    rules.get('required', True)
                )
            elif rules.get('type') == 'number':
                valid, message = Validator.validate_number(
                    value, 
                    rules.get('min_value'), 
                    rules.get('max_value'), 
                    rules.get('required', True)
                )
            elif rules.get('type') == 'date':
                valid, message = Validator.validate_date(
                    value, 
                    rules.get('min_date'), 
                    rules.get('max_date'), 
                    rules.get('required', True)
                )
            elif rules.get('type') == 'dni':
                valid, message = Validator.validate_dni(
                    value, 
                    rules.get('required', True)
                )
            else:
                # Tipo de validación no reconocido
                continue
                
            if not valid:
                errors[field] = message
                
        return errors