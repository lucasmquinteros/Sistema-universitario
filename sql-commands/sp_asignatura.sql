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

CREATE PROCEDURE sp_MoficarAsignatura
    @AsignaturaId INT,
    @Nombre NVARCHAR(128),
    @Hsemanal INT,
    @Htotales INT,
    @Creditos INT,
    @Id_area INT,
    @Id_Regimen INT,
    @Id_depto INT
AS
BEGIN
    SET NOCOUNT ON;
        
        BEGIN TRANSACTION;
        
        BEGIN TRY
            UPDATE Asignatura
            SET 
			Nombre = ISNULL(@Nombre, Nombre),
                Hsemanal = ISNULL(@Hsemanal, Hsemanal),
                Htotales = ISNULL(@Htotales, Htotales),
                Creditos = ISNULL(@Creditos, Creditos),
                Id_area = ISNULL(@Id_area, Id_area),
                Id_Regimen = ISNULL(@Id_Regimen, Id_Regimen),
                Id_depto = ISNULL(@Id_depto, Id_depto)
            WHERE Id = @AsignaturaId;
            
            COMMIT TRANSACTION;
            RETURN 0; 
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION;
            THROW; 
            RETURN ERROR_NUMBER();
        END CATCH
    END
END

CREATE PROCEDURE sp_EliminarAsignatura
    @AsignaturaId INT
AS 
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Eliminar correlativas
        DELETE FROM Correlativa WHERE Id_asignatura = @AsignaturaId;
        
        -- Eliminar asignaturas del plan de estudio
        DELETE FROM AsignaturaxPlan WHERE Id_Asignatura = @AsignaturaId;

        DELETE FROM MateriasxCuatrimestre WHERE Id_Asignatura = @AsignaturaId;

        DELETE FROM ExamenFinal WHERE Id_Asignatura = @AsignaturaId;
        
        -- Eliminar profesores asignados a la asignatura
        DELETE FROM ProfesorxAsignatura WHERE Id_Asignatura = @AsignaturaId;
        
        -- Eliminar la asignatura
        DELETE FROM Asignatura WHERE Id = @AsignaturaId;
        
        COMMIT TRANSACTION;
        RETURN 0; 
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW; 
        RETURN ERROR_NUMBER();
    END CATCH
END

CREATE PROCEDURE sp_AsignarCorrelativa
    @asignatura_id INT,
    @correlativa_id INT
AS
BEGIN
    -- Verificar si la correlativa ya está asignada
    IF EXISTS (SELECT 1 FROM Correlativa WHERE Id_asignatura = @asignatura_id AND Id_Correlativa = @correlativa_id)
    BEGIN
        RAISERROR('La correlativa ya está asignada a esta asignatura.', 16, 1);
        RETURN -1;
        RETURN;
    END

    -- Insertar la nueva correlativa
    INSERT INTO Correlativa (Id_asignatura, Id_Correlativa)
    VALUES (@asignatura_id, @correlativa_id);

END



CREATE PROCEDURE sp_AsignarAsignaturaAPlan
    @asignatura_id INT,
    @plan_id INT,
    @cuatrimestre_id INT
AS
BEGIN
    -- Verificar si la asignatura ya está asignada al plan
    IF EXISTS (SELECT 1 FROM AsignaturaxPlan ap WHERE ap.Id_Asignatura = @asignatura_id AND ap.Id_Plan = @plan_id)
    BEGIN
        RAISERROR('La asignatura ya está asignada a este plan.', 16, 1);
        RETURN -1;
        RETURN;
    END

    -- Insertar la nueva asignación
    INSERT INTO AsignaturaxPlan (Id_Asignatura, Id_Plan)
    VALUES (@asignatura_id, @plan_id);
    INSERT INTO MateriasxCuatrimestre (Id_Asignatura, Id_cuatrimestre)
    VALUES (@asignatura_id, @cuatrimestre_id);

END;


CREATE PROCEDURE sp_ListarAsignaturas
    @Nombre NVARCHAR(128) = NULL,
    @Id_area INT = NULL,
    @Id_Regimen int = NULL,
    @Id_depto INT = NULL,
    @Creditos INT = NULL,
AS
BEGIN 
    SET NOCOUNT ON;

    SELECT Nombre, Hsemanal, Htotales, Creditos FROM Asignatura
    WHERE (@Nombre IS NULL OR Nombre LIKE '%' + @Nombre + '%')
    AND (@Id_area IS NULL OR Id_area = @Id_area)
    AND (@Id_Regimen IS NULL OR Id_Regimen = @Id_Regimen)
    AND (@Id_depto IS NULL OR Id_depto = @Id_depto)
    AND (@Creditos IS NULL OR Creditos = @Creditos);
END