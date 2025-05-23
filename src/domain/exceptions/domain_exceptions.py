class DomainException(Exception):
    """Excepción base para todas las excepciones de dominio"""

    pass


class EntityNotFoundException(DomainException):
    """Excepción lanzada cuando no se encuentra una entidad"""

    def __init__(self, entity_type: str, entity_id: int):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.message = f"No se encontró {entity_type} con ID {entity_id}"
        super().__init__(self.message)


class ValidationException(DomainException):
    """Excepción lanzada cuando falla la validación de una entidad"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class BusinessRuleException(DomainException):
    """Excepción lanzada cuando se viola una regla de negocio"""

    def __init__(self, rule: str, message: str):
        self.rule = rule
        self.message = f"Regla de negocio violada: {rule}. {message}"
        super().__init__(self.message)


class RepositoryException(DomainException):
    """Excepción lanzada cuando ocurre un error en el repositorio"""

    def __init__(self, repository: str, operation: str, message: str):
        self.repository = repository
        self.operation = operation
        self.message = f"Error en repositorio {repository} durante operación {operation}: {message}"
        super().__init__(self.message)
