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


-- UDF to return all of the details of an employee (with validation)

DROP FUNCTION IF EXISTS get_employee_details
GO
CREATE FUNCTION get_employee_details(@emp_num INT)
RETURNS @table TABLE (
    fname                   VARCHAR(15)     NOT NULL,
    lname                   VARCHAR(15)     NOT NULL,
    zip                     VARCHAR(8),
    locality                VARCHAR(20),
    street                  VARCHAR(30),
    [number]                INT,
    birth_date              DATE            NOT NULL,
    sex                     CHAR(1)         NOT NULL,
    establishment_number    INT             NOT NULL,
    schedule_id             INT             NOT NULL,
    private_phone           VARCHAR(15)     NOT NULL,
    company_phone           VARCHAR(15)     NOT NULL	-- "Nums_telem_func" is a multivalue attribute in case in the future we need to associate more than one phone number to the same employee
)
AS
BEGIN
    DECLARE @fname VARCHAR(15);
    DECLARE @lname VARCHAR(15);
    DECLARE @zip VARCHAR(8);
    DECLARE @locality VARCHAR(20);
    DECLARE @street VARCHAR(30);
    DECLARE @number INT;
    DECLARE @birth_date DATE;
    DECLARE @sex CHAR(1);
    DECLARE @establishment_number INT;
    DECLARE @schedule_id INT;
    DECLARE @private_phone VARCHAR(15) = NULL;
    DECLARE @company_phone VARCHAR(15) = NULL;
    DECLARE @phone VARCHAR(9);

    DECLARE emp_cursor CURSOR FOR 
		SELECT Pnome, Unome, cod_postal, localidade, rua, numero, data_nascimento, sexo, num_estabelecimento, id_horario
		FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif 
		WHERE num_funcionario = @emp_num;

    OPEN emp_cursor;
    FETCH NEXT FROM emp_cursor INTO @fname, @lname, @zip, @locality, @street, @number, @birth_date, @sex, @establishment_number, @schedule_id;
    CLOSE emp_cursor;
    DEALLOCATE emp_cursor;

    DECLARE nums_telem_cursor CURSOR FOR 
        SELECT num_telem 
        FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif JOIN Nums_telem_func ON Funcionario.nif = nif_func 
        WHERE num_funcionario = @emp_num;

    OPEN nums_telem_cursor;

    FETCH NEXT FROM nums_telem_cursor INTO @phone;
    WHILE @@FETCH_STATUS = 0
    BEGIN
        IF @phone LIKE '234%'
			BEGIN
				SET @company_phone = @phone;
			END
        ELSE
			BEGIN
				SET @private_phone = @phone;
			END
        FETCH NEXT FROM nums_telem_cursor INTO @phone;
    END

    CLOSE nums_telem_cursor;
    DEALLOCATE nums_telem_cursor;

    INSERT INTO @table (fname, lname, zip, locality, street, [number], birth_date, sex, establishment_number, 
							schedule_id, private_phone, company_phone) 
    VALUES (@fname, @lname, @zip, @locality, @street, @number, @birth_date, @sex, @establishment_number, 
				@schedule_id, @private_phone, @company_phone)

    RETURN
END
GO


-- UDF to return all of the (specific) details of an effective employee (with validation)

DROP FUNCTION IF EXISTS get_effective_details
GO
CREATE FUNCTION get_effective_details(@emp_num INT)
RETURNS @table TABLE (
    fname                   VARCHAR(15)     NOT NULL,
    lname                   VARCHAR(15)     NOT NULL,
    zip                     VARCHAR(8),
    locality                VARCHAR(20),
    street                  VARCHAR(30),
    [number]                INT,
    birth_date              DATE            NOT NULL,
    sex                     CHAR(1)         NOT NULL,
    establishment_number    INT             NOT NULL,
    schedule_id             INT             NOT NULL,
    private_phone           VARCHAR(15)     NOT NULL,
    company_phone           VARCHAR(15)     NOT NULL,
    speciality              VARCHAR(20),
    manager                 BIT
)
AS
BEGIN
    DECLARE @fname VARCHAR(15);
    DECLARE @lname VARCHAR(15);
    DECLARE @zip VARCHAR(8);
    DECLARE @locality VARCHAR(20);
    DECLARE @street VARCHAR(30);
    DECLARE @number INT;
    DECLARE @birth_date DATE;
    DECLARE @sex CHAR(1);
    DECLARE @establishment_number INT;
    DECLARE @schedule_id INT;
    DECLARE @private_phone VARCHAR(15) = NULL;
    DECLARE @company_phone VARCHAR(15) = NULL;
    DECLARE @speciality VARCHAR(20);
    DECLARE @manager BIT = 0;
    DECLARE @phone VARCHAR(9);

    DECLARE effective_cursor CURSOR FOR 
		SELECT Pnome, Unome, cod_postal, localidade, rua, numero, data_nascimento, sexo, num_estabelecimento, id_horario, especialidade 
		FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif JOIN Efetivo ON Funcionario.nif = Efetivo.nif LEFT JOIN Tem ON Efetivo.nif = nif_efetivo 
		WHERE num_funcionario = @emp_num;

    OPEN effective_cursor;
    FETCH NEXT FROM effective_cursor INTO @fname, @lname, @zip, @locality, @street, @number, @birth_date, @sex, @establishment_number, @schedule_id, @speciality;
    CLOSE effective_cursor;
    DEALLOCATE effective_cursor;

    IF EXISTS (SELECT num_funcionario 
				FROM Estabelecimento JOIN Pessoa ON nif_gerente = Pessoa.nif JOIN Funcionario ON Pessoa.nif = Funcionario.nif 
				WHERE num_funcionario = @emp_num)
		BEGIN
			SET @manager = 1;
		END

    DECLARE nums_telem_cursor CURSOR FOR 
        SELECT num_telem 
        FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif JOIN Nums_telem_func ON Funcionario.nif = nif_func 
        WHERE num_funcionario = @emp_num;

    OPEN nums_telem_cursor;

    FETCH NEXT FROM nums_telem_cursor INTO @phone;
    WHILE @@FETCH_STATUS = 0
    BEGIN
        IF @phone LIKE '234%'
			BEGIN
				SET @company_phone = @phone;
			END
        ELSE 
			BEGIN
				SET @private_phone = @phone;
			END
        FETCH NEXT FROM nums_telem_cursor INTO @phone;
    END

    CLOSE nums_telem_cursor;
    DEALLOCATE nums_telem_cursor;

    INSERT INTO @table (fname, lname, zip, locality, street, [number], birth_date, sex, establishment_number, 
							schedule_id, private_phone, company_phone, speciality, manager) 
    VALUES (@fname, @lname, @zip, @locality, @street, @number, @birth_date, @sex, @establishment_number, 
				@schedule_id, @private_phone, @company_phone, @speciality, @manager)

    RETURN
END
GO
