-- Eliminar as udf

IF OBJECT_ID('get_employee_performance') IS NOT NULL
DROP FUNCTION get_employee_performance;
GO


-- UDF para retornar a performance de um employee

CREATE FUNCTION get_employee_performance(@nif INT)
RETURNS VARCHAR(50)
AS
BEGIN
    DECLARE @average_rating FLOAT;
    DECLARE @performance VARCHAR(50);
    SELECT @average_rating = AVG(CAST(n_estrelas AS FLOAT)) FROM Avaliacao WHERE nif_funcionario = @nif;

    IF @average_rating > 4
        SET @performance = 'Excelent';
    ELSE IF @average_rating > 3
        SET @performance = 'Good';
    ELSE IF @average_rating > 2
        SET @performance = 'Average';
    ELSE IF @average_rating > 1
        SET @performance = 'Poor';
    ELSE
        SET @performance = 'Very Poor';
    RETURN @performance;
END
GO