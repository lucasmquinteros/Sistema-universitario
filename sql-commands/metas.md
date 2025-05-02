## Lista Completa de Stored Procedures Necesarios

### 1. Gestión de Alumnos

- ✅ `sp_CrearAlumno` - Crear un nuevo alumno
- ✅ `sp_ObtenerAlumno` - Obtener datos de un alumno por ID
- ✅ `sp_ModificarAlumno` - Actualizar datos de un alumno
- ✅ `sp_EliminarAlumno` - Eliminar un alumno (baja lógica)
- ✅ `sp_ListarAlumnos` - Listar alumnos con filtros
- 🔲 `sp_InscribirAlumnoCarrera` - Inscribir alumno a una carrera
- 🔲 `sp_ObtenerCursadasAlumno` - Obtener materias que cursa un alumno

### 2. Gestión de Profesores

- ✅ `sp_CrearProfesor` - Crear un nuevo profesor
- ✅ `sp_ObtenerProfesor` - Obtener datos de un profesor por ID
- ✅ `sp_ListarProfesores` - Listar profesores con filtros
- ✅ `sp_AsignarProfesorAsignatura` - Asignar profesor a una asignatura
- 🔲 `sp_ModificarProfesor` - Actualizar datos de un profesor
- 🔲 `sp_EliminarProfesor` - Eliminar un profesor (baja lógica)
- 🔲 `sp_ObtenerAsignaturasProfesor` - Obtener asignaturas de un profesor

### 3. Gestión de Asignaturas

- ✅ `sp_CrearAsignatura` - Crear una nueva asignatura
- ✅ `sp_ObtenerAsignatura` - Obtener datos de una asignatura por ID
- 🔲 `sp_ModificarAsignatura` - Actualizar datos de una asignatura
- 🔲 `sp_EliminarAsignatura` - Eliminar una asignatura
- 🔲 `sp_ListarAsignaturas` - Listar asignaturas con filtros
- 🔲 `sp_AgregarCorrelativa` - Agregar correlativa a una asignatura
- 🔲 `sp_AsignarAsignaturaAPlan` - Asignar asignatura a un plan de estudios

### 4. Gestión de Carreras y Planes de Estudio

- 🔲 `sp_CrearCarrera` - Crear una nueva carrera
- 🔲 `sp_ObtenerCarrera` - Obtener datos de una carrera por ID
- 🔲 `sp_ModificarCarrera` - Actualizar datos de una carrera
- 🔲 `sp_CrearPlanEstudio` - Crear un nuevo plan de estudios
- 🔲 `sp_ObtenerPlanEstudio` - Obtener datos de un plan de estudios
- 🔲 `sp_ObtenerAsignaturasPlan` - Obtener asignaturas de un plan

### 5. Gestión de Usuarios y Permisos

- 🔲 `sp_CrearUsuario` - Crear un nuevo usuario
- 🔲 `sp_AutenticarUsuario` - Autenticar un usuario
- 🔲 `sp_AsignarRolUsuario` - Asignar rol a un usuario
- 🔲 `sp_VerificarPermiso` - Verificar si un usuario tiene un permiso
- 🔲 `sp_CambiarPassword` - Cambiar contraseña de usuario
- 🔲 `sp_ListarUsuarios` - Listar usuarios con filtros

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

## Clases Pendientes por Implementar

### 1. Modelos

- ✅ `Entidad` - Clase base para todas las entidades
- ✅ `Profesor` - Modelo de profesor
- ✅ `Alumno` - Modelo de alumno
- ✅ `Asignatura` - Modelo de asignatura
- 🔲 `Carrera` - Modelo de carrera
- 🔲 `PlanEstudio` - Modelo de plan de estudios
- 🔲 `Usuario` - Modelo de usuario
- 🔲 `Rol` - Modelo de rol
- 🔲 `Permiso` - Modelo de permiso
- 🔲 `Cursada` - Modelo de cursada
- 🔲 `Examen` - Modelo de examen

### 2. Servicios

- ✅ `BaseService` - Clase base para todos los servicios
- ✅ `ProfesorService` - Servicio para gestión de profesores
- ✅ `AlumnoService` - Servicio para gestión de alumnos
- ✅ `AsignaturaService` - Servicio para gestión de asignaturas
- 🔲 `CarreraService` - Servicio para gestión de carreras
- 🔲 `PlanEstudioService` - Servicio para gestión de planes de estudio
- 🔲 `UsuarioService` - Servicio para gestión de usuarios
- 🔲 `CursadaService` - Servicio para gestión de cursadas
- 🔲 `ExamenService` - Servicio para gestión de exámenes
- 🔲 `ReporteService` - Servicio para generación de reportes

### 3. Utilidades

- ✅ `DatabaseManager` - Gestor de conexiones a la base de datos
- ✅ `Logger` - Sistema de registro de actividades
- 🔲 `Validator` - Validador de datos
- 🔲 `ConfigManager` - Gestor de configuración
- 🔲 `SecurityManager` - Gestor de seguridad (hash de contraseñas, etc.)

## Métodos Adicionales por Implementar

### 1. En AlumnoService

- `inscribir_carrera(alumno_id, carrera_id)` - Inscribir alumno a una carrera
- `inscribir_asignatura(alumno_id, asignatura_id, año_academico, cuatrimestre)` - Inscribir alumno a una asignatura
- `registrar_nota(alumno_id, asignatura_id, nota, tipo_examen)` - Registrar nota de un alumno
- `obtener_historial_academico(alumno_id)` - Obtener historial académico de un alumno
- `verificar_correlativas(alumno_id, asignatura_id)` - Verificar si un alumno cumple correlativas

### 2. En ProfesorService

- `registrar_asistencia(profesor_id, fecha, estado)` - Registrar asistencia de un profesor
- `obtener_carga_horaria(profesor_id, año_academico, cuatrimestre)` - Obtener carga horaria de un profesor
- `calificar_alumno(profesor_id, alumno_id, asignatura_id, nota, tipo_examen)` - Calificar a un alumno

### 3. En AsignaturaService

- `agregar_correlativa(asignatura_id, correlativa_id)` - Agregar correlativa a una asignatura
- `asignar_a_plan(asignatura_id, plan_id, año, cuatrimestre)` - Asignar asignatura a un plan de estudios
- `obtener_estadisticas(asignatura_id, año_academico, cuatrimestre)` - Obtener estadísticas de una asignatura

### 4. En UsuarioService

- `autenticar(username, password)` - Autenticar un usuario
- `cambiar_password(usuario_id, password_actual, nueva_password)` - Cambiar contraseña
- `asignar_rol(usuario_id, rol_id)` - Asignar rol a un usuario
- `verificar_permiso(usuario_id, codigo_permiso)` - Verificar si un usuario tiene un permiso
