CREATE PROCEDURE sp_EliminarAlumno
    @id INT,
    @DNI NVARCHAR(20)
AS
BEGIN 
    SET NOCOUNT ON;
   
    IF NOT EXISTS (SELECT 1 FROM Alumno WHERE id = @id AND DNI = @DNI)
    BEGIN
        RETURN -1;
    END
    
    BEGIN TRY
        BEGIN TRANSACTION;
        

        DELETE FROM InscripcionExamen WHERE Id_Alumno = @id;
        DELETE FROM Cursada WHERE Id_Alumno = @id;
        DELETE FROM AlumnoxCarrera WHERE Id_Alumno = @id;
        DELETE FROM Alumno WHERE Id = @id;
        
        COMMIT TRANSACTION;
        
        RETURN 0; 
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
            
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();
        RAISERROR('Error en sp_EliminarAlumno (ID: %d): %s', 
                 @ErrorSeverity, 
                 @ErrorState,
                 @id,
                 @ErrorMessage);
        RETURN ERROR_NUMBER();
    END CATCH
END

CREATE PROCEDURE sp_AutenticarUsuario
    @Username NVARCHAR(50),
    @PasswordHash NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Verificar credenciales
    DECLARE @UserId INT;
    DECLARE @Estado NVARCHAR(20);
    
    SELECT @UserId = Id, @Estado = Estado
    FROM Usuario
    WHERE Username = @Username AND PasswordHash = @PasswordHash;
    
    IF @UserId IS NULL
    BEGIN
        -- Usuario no encontrado o contraseña incorrecta
        RETURN -1;
    END
    
    IF @Estado <> 'Activo'
    BEGIN
        -- Usuario no activo
        RETURN -2;
    END
    
    -- Actualizar último acceso
    UPDATE Usuario 
    SET UltimoAcceso = GETDATE(), IntentosFallidos = 0
    WHERE Id = @UserId;
    
    -- Devolver información del usuario
    SELECT Id, Username, Email, Estado
    FROM Usuario
    WHERE Id = @UserId;
    
    -- Devolver roles del usuario
    SELECT r.Id, r.Nombre, r.NivelAcceso
    FROM Rol r
    JOIN UsuarioRol ur ON r.Id = ur.Id_Rol
    WHERE ur.Id_Usuario = @UserId;
    
    -- Devolver entidades vinculadas
    SELECT TipoEntidad, Id_Entidad
    FROM UsuarioEntidad
    WHERE Id_Usuario = @UserId;
    
    -- Devolver permisos del usuario
    SELECT DISTINCT p.Id, p.Codigo, p.Nombre, p.Modulo
    FROM Permiso p
    JOIN RolPermiso rp ON p.Id = rp.Id_Permiso
    JOIN UsuarioRol ur ON rp.Id_Rol = ur.Id_Rol
    WHERE ur.Id_Usuario = @UserId;
    
    RETURN 0; -- Éxito
END

-- Crear Alumno
CREATE PROCEDURE sp_CrearAlumno
    @Nombre NVARCHAR(128),
    @Apellido NVARCHAR(128),
    @DNI NVARCHAR(20),
    @FechaNacimiento DATE,
    @Email NVARCHAR(128),
    @Telefono NVARCHAR(20) = NULL,
    @Direccion NVARCHAR(255) = NULL,
    @FechaIngreso DATE = NULL,
    @CarreraId INT = NULL,
    @AlumnoId INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validar que el DNI no exista
    IF EXISTS (SELECT 1 FROM Alumno WHERE DNI = @DNI)
    BEGIN
        RAISERROR('Ya existe un alumno con ese DNI', 16, 1);
        RETURN -1;
    END
    
    -- Establecer fecha de ingreso si no se proporciona
    IF @FechaIngreso IS NULL
        SET @FechaIngreso = GETDATE();
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Insertar alumno
        INSERT INTO Alumno (Nombre, Apellido, DNI, FechaNacimiento, Email, 
                           Telefono, Direccion, FechaIngreso, Estado)
        VALUES (@Nombre, @Apellido, @DNI, @FechaNacimiento, @Email,
               @Telefono, @Direccion, @FechaIngreso, 'Activo');
        
        -- Obtener ID generado
        SET @AlumnoId = SCOPE_IDENTITY();
        
        -- Si se proporciona carrera, inscribir al alumno
        IF @CarreraId IS NOT NULL
        BEGIN
            INSERT INTO AlumnoxCarrera (Id_Alumno, Id_Carrera, FechaInscripcion)
            VALUES (@AlumnoId, @CarreraId, GETDATE());
        END
        
        COMMIT TRANSACTION;
        RETURN 0; -- Éxito
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW; -- Re-lanzar la excepción
        RETURN ERROR_NUMBER();
    END CATCH
END

-- Obtener Alumno
CREATE PROCEDURE sp_ObtenerAlumno
    @AlumnoId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Datos básicos del alumno
    SELECT * FROM Alumno WHERE Id = @AlumnoId;
    
    -- Carreras del alumno
    SELECT c.Id, c.Nombre, ac.FechaInscripcion
    FROM Carrera c
    JOIN AlumnoxCarrera ac ON c.Id = ac.Id_Carrera
    WHERE ac.Id_Alumno = @AlumnoId;
    
    -- Cursadas actuales
    SELECT a.Id, a.Nombre, c.Estado, c.NotaFinal
    FROM Asignatura a
    JOIN Cursada c ON a.Id = c.Id_Asignatura
    WHERE c.Id_Alumno = @AlumnoId AND c.Estado = 'Cursando';
    
    -- Usuario asociado
    SELECT u.Id, u.Username, u.Email
    FROM Usuario u
    JOIN UsuarioEntidad ue ON u.Id = ue.Id_Usuario
    WHERE ue.TipoEntidad = 'Alumno' AND ue.Id_Entidad = @AlumnoId;
    
    RETURN 0;
END

-- Modificar Alumno
CREATE PROCEDURE sp_ModificarAlumno
    @AlumnoId INT,
    @Nombre NVARCHAR(128) = NULL,
    @Apellido NVARCHAR(128) = NULL,
    @Email NVARCHAR(128) = NULL,
    @Telefono NVARCHAR(20) = NULL,
    @Direccion NVARCHAR(255) = NULL,
    @Estado NVARCHAR(20) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Verificar que el alumno existe
    IF NOT EXISTS (SELECT 1 FROM Alumno WHERE Id = @AlumnoId)
    BEGIN
        RAISERROR('El alumno no existe', 16, 1);
        RETURN -1;
    END
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Actualizar solo los campos proporcionados
        UPDATE Alumno
        SET 
            Nombre = ISNULL(@Nombre, Nombre),
            Apellido = ISNULL(@Apellido, Apellido),
            Email = ISNULL(@Email, Email),
            Telefono = ISNULL(@Telefono, Telefono),
            Direccion = ISNULL(@Direccion, Direccion),
            Estado = ISNULL(@Estado, Estado)
        WHERE Id = @AlumnoId;
        
        -- Si se actualizó el email, actualizar también en Usuario si existe
        IF @Email IS NOT NULL
        BEGIN
            UPDATE u
            SET u.Email = @Email
            FROM Usuario u
            JOIN UsuarioEntidad ue ON u.Id = ue.Id_Usuario
            WHERE ue.TipoEntidad = 'Alumno' AND ue.Id_Entidad = @AlumnoId;
        END
        
        -- Si se cambió el estado a inactivo, actualizar usuario
        IF @Estado = 'Inactivo'
        BEGIN
            UPDATE u
            SET u.Estado = 'Inactivo'
            FROM Usuario u
            JOIN UsuarioEntidad ue ON u.Id = ue.Id_Usuario
            WHERE ue.TipoEntidad = 'Alumno' AND ue.Id_Entidad = @AlumnoId;
        END
        
        COMMIT TRANSACTION;
        RETURN 0; -- Éxito
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
        RETURN ERROR_NUMBER();
    END CATCH
END

-- Crear Profesor
CREATE PROCEDURE sp_CrearProfesor
    @Nombre NVARCHAR(128),
    @Apellido NVARCHAR(128),
    @DNI NVARCHAR(20),
    @Email NVARCHAR(128),
    @Telefono NVARCHAR(20) = NULL,
    @Titulo NVARCHAR(128),
    @Especialidad NVARCHAR(128) = NULL,
    @TipoContrato NVARCHAR(50),
    @FechaIngreso DATE = NULL,
    @Id_Departamento INT,
    @ProfesorId INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validar que el DNI no exista
    IF EXISTS (SELECT 1 FROM Profesor WHERE DNI = @DNI)
    BEGIN
        RAISERROR('Ya existe un profesor con ese DNI', 16, 1);
        RETURN -1;
    END
    
    -- Establecer fecha de ingreso si no se proporciona
    IF @FechaIngreso IS NULL
        SET @FechaIngreso = GETDATE();
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Insertar profesor
        INSERT INTO Profesor (Nombre, Apellido, DNI, Email, Telefono, 
                             Titulo, Especialidad, TipoContrato, FechaIngreso, Id_Departamento)
        VALUES (@Nombre, @Apellido, @DNI, @Email, @Telefono,
               @Titulo, @Especialidad, @TipoContrato, @FechaIngreso, @Id_Departamento);
        
        -- Obtener ID generado
        SET @ProfesorId = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
        RETURN 0; -- Éxito
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW; -- Re-lanzar la excepción
        RETURN ERROR_NUMBER();
    END CATCH
END

-- Obtener Profesor
CREATE PROCEDURE sp_ObtenerProfesor
    @ProfesorId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Datos básicos del profesor con nombre del departamento
    SELECT p.*, d.Nombre AS Departamento
    FROM Profesor p
    LEFT JOIN Departamento d ON p.Id_Departamento = d.Id
    WHERE p.Id = @ProfesorId;
    
    -- Asignaturas que imparte
    SELECT a.Id, a.Nombre, pa.Rol, pa.AñoAcademico, pa.Cuatrimestre
    FROM Asignatura a
    JOIN ProfesorxAsignatura pa ON a.Id = pa.Id_Asignatura
    WHERE pa.Id_Profesor = @ProfesorId;
    
    RETURN 0;
END

-- Listar Profesores
CREATE PROCEDURE sp_ListarProfesores
    @DepartamentoId INT = NULL,
    @Especialidad NVARCHAR(128) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT p.*, d.Nombre AS Departamento
    FROM Profesor p
    LEFT JOIN Departamento d ON p.Id_Departamento = d.Id
    WHERE (@DepartamentoId IS NULL OR p.Id_Departamento = @DepartamentoId)
      AND (@Especialidad IS NULL OR p.Especialidad LIKE '%' + @Especialidad + '%')
    ORDER BY p.Apellido, p.Nombre;
    
    RETURN 0;
END

-- Asignar Profesor a Asignatura
CREATE PROCEDURE sp_AsignarProfesorAsignatura
    @ProfesorId INT,
    @AsignaturaId INT,
    @Rol NVARCHAR(50),
    @AñoAcademico INT,
    @Cuatrimestre INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Verificar que el profesor existe
    IF NOT EXISTS (SELECT 1 FROM Profesor WHERE Id = @ProfesorId)
    BEGIN
        RAISERROR('El profesor no existe', 16, 1);
        RETURN -1;
    END
    
    -- Verificar que la asignatura existe
    IF NOT EXISTS (SELECT 1 FROM Asignatura WHERE Id = @AsignaturaId)
    BEGIN
        RAISERROR('La asignatura no existe', 16, 1);
        RETURN -2;
    END
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Verificar si ya existe la asignación
        IF EXISTS (
            SELECT 1 
            FROM ProfesorxAsignatura 
            WHERE Id_Profesor = @ProfesorId 
              AND Id_Asignatura = @AsignaturaId
              AND AñoAcademico = @AñoAcademico
              AND Cuatrimestre = @Cuatrimestre
        )
        BEGIN
            -- Actualizar rol si ya existe
            UPDATE ProfesorxAsignatura
            SET Rol = @Rol
            WHERE Id_Profesor = @ProfesorId 
              AND Id_Asignatura = @AsignaturaId
              AND AñoAcademico = @AñoAcademico
              AND Cuatrimestre = @Cuatrimestre;
        END
        ELSE
        BEGIN
            -- Insertar nueva asignación
            INSERT INTO ProfesorxAsignatura (Id_Profesor, Id_Asignatura, Rol, AñoAcademico, Cuatrimestre)
            VALUES (@ProfesorId, @AsignaturaId, @Rol, @AñoAcademico, @Cuatrimestre);
        END
        
        COMMIT TRANSACTION;
        RETURN 0; -- Éxito
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW; -- Re-lanzar la excepción
        RETURN ERROR_NUMBER();
    END CATCH
END

-- Crear Asignatura
CREATE PROCEDURE sp_CrearAsignatura
    @Nombre NVARCHAR(128),
    @Hsemanal INT,
    @Htotales INT,
    @Creditos INT,
    @Id_area INT,
    @Id_Regimen INT,
    @Id_depto INT,
    @AsignaturaId INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Insertar asignatura
        INSERT INTO Asignatura (Nombre, Hsemanal, Htotales, Creditos, Id_area, Id_Regimen, Id_depto)
        VALUES (@Nombre, @Hsemanal, @Htotales, @Creditos, @Id_area, @Id_Regimen, @Id_depto);
        
        -- Obtener ID generado
        SET @AsignaturaId = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
        RETURN 0; -- Éxito
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW; -- Re-lanzar la excepción
        RETURN ERROR_NUMBER();
    END CATCH
END

-- Obtener Asignatura
CREATE PROCEDURE sp_ObtenerAsignatura
    @AsignaturaId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Datos básicos de la asignatura con nombres relacionados
    SELECT a.*,
           ar.Nombre AS Area,
           r.Nombre AS Regimen,
           d.Nombre AS Departamento
    FROM Asignatura a
    LEFT JOIN Area ar ON a.Id_area = ar.Id
    LEFT JOIN Regimen r ON a.Id_Regimen = r.Id
    LEFT JOIN Departamento d ON a.Id_depto = d.Id
    WHERE a.Id = @AsignaturaId;
    
    -- Profesores que la imparten actualmente
    SELECT p.Id, p.Nombre, p.Apellido, pa.Rol, pa.AñoAcademico, pa.Cuatrimestre
    FROM Profesor p
    JOIN ProfesorxAsignatura pa ON p.Id = pa.Id_Profesor
    WHERE pa.Id_Asignatura = @AsignaturaId
    AND pa.AñoAcademico = YEAR(GETDATE())
    ORDER BY pa.Rol;
    
    -- Planes de estudio que la incluyen
    SELECT pe.Id, pe.Nombre, pe.Año
    FROM PlanEstudio pe
    JOIN AsignaturaxPlan ap ON pe.Id = ap.Id_Plan
    WHERE ap.Id_Asignatura = @AsignaturaId;
    
    -- Correlativas (prerrequisitos)
    SELECT a2.Id, a2.Nombre
    FROM Asignatura a2
    JOIN Correlativa c ON a2.Id = c.Id_Correlativa
    WHERE c.Id_asignatura = @AsignaturaId;
    
    RETURN 0;
END

-- Crear Usuario
CREATE PROCEDURE sp_CrearUsuario
    @Username NVARCHAR(50),
    @Password NVARCHAR(256), -- Hash de la contraseña
    @Email NVARCHAR(128),
    @Nombre NVARCHAR(128),
    @Apellido NVARCHAR(128),
    @FechaCreacion DATETIME = NULL,
    @Activo BIT = 1,
    @UsuarioId INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validar que el username no exista
    IF EXISTS (SELECT 1 FROM Usuario WHERE Username = @Username)
    BEGIN
        RAISERROR('El nombre de usuario ya existe', 16, 1);
        RETURN -1;
    END
    
    -- Establecer fecha de creación si no se proporciona
    IF @FechaCreacion IS NULL
        SET @FechaCreacion = GETDATE();
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Insertar usuario
        INSERT INTO Usuario (Username, Password, Email, Nombre, Apellido, FechaCreacion, Activo)
        VALUES (@Username, @Password, @Email, @Nombre, @Apellido, @FechaCreacion, @Activo);
        
        -- Obtener ID generado
        SET @UsuarioId = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
        RETURN 0; -- Éxito
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW; -- Re-lanzar la excepción
        RETURN ERROR_NUMBER();
    END CATCH
END

-- Autenticar Usuario
CREATE PROCEDURE sp_AutenticarUsuario
    @Username NVARCHAR(50),
    @Password NVARCHAR(256) -- Hash de la contraseña
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Verificar credenciales y devolver información del usuario
    SELECT u.Id, u.Username, u.Email, u.Nombre, u.Apellido, u.FechaCreacion, u.Activo
    FROM Usuario u
    WHERE u.Username = @Username AND u.Password = @Password AND u.Activo = 1;
    
    -- Devolver roles del usuario
    SELECT r.Id, r.Nombre, r.Descripcion
    FROM Rol r
    JOIN UsuarioxRol ur ON r.Id = ur.Id_Rol
    WHERE ur.Id_Usuario = (SELECT Id FROM Usuario WHERE Username = @Username);
    
    -- Devolver permisos del usuario
    SELECT p.Id, p.Codigo, p.Descripcion
    FROM Permiso p
    JOIN RolxPermiso rp ON p.Id = rp.Id_Permiso
    JOIN UsuarioxRol ur ON rp.Id_Rol = ur.Id_Rol
    WHERE ur.Id_Usuario = (SELECT Id FROM Usuario WHERE Username = @Username);
    
    RETURN 0;
END

-- Asignar Rol a Usuario
CREATE PROCEDURE sp_AsignarRolUsuario
    @UsuarioId INT,
    @RolId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Verificar que el usuario existe
    IF NOT EXISTS (SELECT 1 FROM Usuario WHERE Id = @UsuarioId)
    BEGIN
        RAISERROR('El usuario no existe', 16, 1);
        RETURN -1;
    END
    
    -- Verificar que el rol existe
    IF NOT EXISTS (SELECT 1 FROM Rol WHERE Id = @RolId)
    BEGIN
        RAISERROR('El rol no existe', 16, 1);
        RETURN -2;
    END
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Verificar si ya existe la asignación
        IF EXISTS (
            SELECT 1 
            FROM UsuarioxRol 
            WHERE Id_Usuario = @UsuarioId AND Id_Rol = @RolId
        )
        BEGIN
            -- Ya existe, no hacer nada
            COMMIT TRANSACTION;
            RETURN 0;
        END
        ELSE
        BEGIN
            -- Insertar nueva asignación
            INSERT INTO UsuarioxRol (Id_Usuario, Id_Rol)
            VALUES (@UsuarioId, @RolId);
        END
        
        COMMIT TRANSACTION;
        RETURN 0; -- Éxito
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW; -- Re-lanzar la excepción
        RETURN ERROR_NUMBER();
    END CATCH
END

CREATE PROCEDURE sp_ListarAlumnos
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        A.Id,
        A.DNI,
        A.Nombre,
        A.Apellido,
        CASE 
            WHEN A.Email IS NULL THEN 'No proporcionado'
            ELSE A.Email
        END AS Email,
        CASE
            WHEN C.Nombre IS NULL THEN 'Carrera no asignada'
            WHEN C.Nombre = '' THEN 'Carrera en proceso'
            ELSE C.Nombre
        END AS NombreCarrera,
        A.FechaIngreso,
        A.Estado
    FROM 
        Alumno A
    LEFT JOIN 
        AlumnoxCarrera AC ON A.Id = AC.Id_Alumno
    LEFT JOIN
        Carrera C ON AC.Id_Carrera = C.Id
    ORDER BY 
        A.Apellido, A.Nombre;
END