## Lista Completa de Stored Procedures Necesarios

### 1. Gestión de Alumnos

- ✅ `sp_CrearAlumno` - Crear un nuevo alumno
- ✅ `sp_ModificarAlumno` - Actualizar datos de un alumno
- ✅ `sp_EliminarAlumno` - Eliminar un alumno (baja lógica)
- 🔲 `sp_InscribirAlumnoCarrera` - Inscribir alumno a una carrera
- 🔲 `sp_ObtenerCursadasAlumno` - Obtener materias que cursa un alumno

### 2. Gestión de Profesores

- ✅ `sp_CrearProfesor` - Crear un nuevo profesor
- ✅ `sp_AsignarProfesorAsignatura` - Asignar profesor a una asignatura
- 🔲 `sp_ModificarProfesor` - Actualizar datos de un profesor
- 🔲 `sp_EliminarProfesor` - Eliminar un profesor (baja lógica)
- 🔲 `sp_ObtenerAsignaturasProfesor` - Obtener asignaturas de un profesor

### 3. Gestión de Asignaturas

- ✅ `sp_CrearAsignatura` - Crear una nueva asignatura
- ✅ `sp_ObtenerAsignatura` - Obtener datos de una asignatura por ID
- 🔲 `sp_ModificarAsignatura` - Actualizar datos de una asignatura
- 🔲 `sp_EliminarAsignatura` - Eliminar una asignatura
- 🔲 `sp_AgregarCorrelativa` - Agregar correlativa a una asignatura
- 🔲 `sp_AsignarAsignaturaAPlan` - Asignar asignatura a un plan de estudios

### 4. Gestión de Carreras y Planes de Estudio

- 🔲 `sp_CrearCarrera` - Crear una nueva carrera
- 🔲 `sp_ModificarCarrera` - Actualizar datos de una carrera
- 🔲 `sp_CrearPlanEstudio` - Crear un nuevo plan de estudios
- 🔲 `sp_ObtenerAsignaturasPlan` - Obtener asignaturas de un plan

### 5. Gestión de Usuarios y Permisos

- 🔲 `sp_CrearUsuario` - Crear un nuevo usuario
- 🔲 `sp_AutenticarUsuario` - Autenticar un usuario
- 🔲 `sp_AsignarRolUsuario` - Asignar rol a un usuario
- 🔲 `sp_VerificarPermiso` - Verificar si un usuario tiene un permiso
- 🔲 `sp_CambiarPassword` - Cambiar contraseña de usuario

### 6. Gestión de Inscripciones y Cursadas

- 🔲 `sp_InscribirAlumnoAsignatura` - Inscribir alumno a una asignatura
- 🔲 `sp_RegistrarNota` - Registrar nota de un alumno
- 🔲 `sp_ObtenerHistorialAcademico` - Obtener historial académico de un alumno
- 🔲 `sp_VerificarCorrelativas` - Verificar si un alumno cumple correlativas

### 7. Reportes y Estadísticas

- 🔲 `sp_ReporteRendimientoAcademico` - Reporte de rendimiento académico
- 🔲 `sp_ReporteAsistenciasProfesores` - Reporte de asistencias de profesores
- 🔲 `sp_ReporteInscripcionesPorCarrera` - Reporte de inscripciones por carrera
- 🔲 `sp_ReporteAprobacionPorAsignatura` - Reporte de aprobación por asignatura

### Fase 1: Infraestructura Base

- ✅ Implementar modelos (Models)
- ✅ Implementar utilidades (Utils)
- 🔲 Configurar SQLAlchemy
- 🔲 Implementar DatabaseManager híbrido
- 🔲 Implementar sistema de logging para API

### Fase 2: API y Servicios

- 🔲 Configurar FastAPI
- 🔲 Implementar autenticación JWT
- 🔲 Crear endpoints básicos
- 🔲 Implementar validación con Pydantic
- 🔲 Documentar API con Swagger/OpenAPI

### Fase 3: Gestión Académica

- 🔲 Implementar servicios con SQLAlchemy
- 🔲 Mantener SPs para operaciones de escritura
- 🔲 Crear endpoints para gestión académica
- 🔲 Implementar lógica de negocio en servicios
- 🔲 Optimizar consultas complejas

### Fase 4: Frontend

- 🔲 Configurar framework frontend (React, Vue, etc.)
- 🔲 Implementar autenticación en frontend
- 🔲 Crear interfaces de usuario
- 🔲 Conectar con API
- 🔲 Implementar validaciones en cliente

### Fase 5: Mejoras y Despliegue

- 🔲 Implementar tests unitarios
- 🔲 Configurar CI/CD
- 🔲 Optimizar rendimiento
- 🔲 Implementar caché
- 🔲 Preparar para producción

## Próximos Pasos Inmediatos

1. **Configurar SQLAlchemy**: Implementar la configuración de SQLAlchemy y los modelos ORM.
2. **Implementar DatabaseManager híbrido**: Crear un gestor de base de datos que combine SQLAlchemy y stored procedures.
3. **Configurar FastAPI**: Implementar la estructura básica de la API con FastAPI.
4. **Implementar autenticación JWT**: Configurar el sistema de autenticación con tokens JWT.
5. **Crear endpoints básicos**: Implementar los endpoints para las operaciones CRUD básicas.
