

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
CREATE PROCEDURE sp_CrearUsuario --REVISAR
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


CREATE PROCEDURE InsertarInscripcionExamen(
    IN pIdAlumno INTEGER,
    IN pIdExamenFinal INTEGER,
    IN pEstado VARCHAR(255),
    IN pCalificacion DECIMAL(10,2),
    IN pObservaciones TEXT
)
BEGIN
    -- Validar que el alumno exista
    IF NOT EXISTS (SELECT 1 FROM Alumno WHERE Id = pIdAlumno) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El alumno no existe.';
    
    -- Validar que el examen final exista
    ELSEIF NOT EXISTS (SELECT 1 FROM ExamenFinal WHERE Id = pIdExamenFinal) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El examen final no existe.';
    
    ELSE
        INSERT INTO InscripcionExamen (
            Id_Alumno,
            Id_ExamenFinal,
            Estado,
            Calificacion,
            Observaciones
        )
        VALUES (
            pIdAlumno,
            pIdExamenFinal,
            pEstado,
            pCalificacion,
            pObservaciones
        );
    END IF;
END 


