-- Eliminar as udf

IF OBJECT_ID('get_employee_performance') IS NOT NULL
DROP FUNCTION get_employee_performance;
GO

IF OBJECT_ID('get_appointment_details') IS NOT NULL
DROP FUNCTION get_appointment_details;
GO


-- UDF to return the performance of an employee based on the average rating of their reviews

CREATE FUNCTION get_employee_performance(@nif INT)
RETURNS VARCHAR(50)
AS
BEGIN
    DECLARE @average_rating FLOAT;
    DECLARE @performance VARCHAR(50);
    SELECT @average_rating = AVG(CAST(n_estrelas AS FLOAT)) 
    FROM Avaliacao WHERE nif_funcionario = @nif;

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


-- UDF to return all of the details of an appointment

CREATE FUNCTION get_appointment_details(@nif_emp INT, @nif_cli INT, @date DATETIME)
RETURNS table
AS
RETURN (
    SELECT *
    FROM viewAppointmentDetails
    WHERE nif_funcionario = @nif_emp 
    AND nif_cliente = @nif_cli 
    AND data_marcacao = @date
);
GO


-- UDF to return all of the details of an employee (with validation)

DROP FUNCTION IF EXISTS get_employee_details
GO
CREATE FUNCTION get_employee_details(@emp_num INT)
RETURNS @table TABLE (
	nif						INT				NOT NULL,
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
    private_phone           INT             NOT NULL,
    company_phone           INT             NOT NULL	-- "Nums_telem_func" is a multivalue attribute in case in the future we need to associate more than one phone number to the same employee
)
AS
BEGIN
	DECLARE @nif INT;
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
    DECLARE @private_phone INT;
    DECLARE @company_phone INT;
    DECLARE @phone VARCHAR(9);

    DECLARE emp_cursor CURSOR FOR 
		SELECT Pessoa.nif, Pnome, Unome, cod_postal, localidade, rua, numero, data_nascimento, sexo, num_estabelecimento, id_horario
		FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif 
		WHERE num_funcionario = @emp_num;

    OPEN emp_cursor;
    FETCH NEXT FROM emp_cursor INTO @nif, @fname, @lname, @zip, @locality, @street, @number, @birth_date, @sex, @establishment_number, @schedule_id;
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

    INSERT INTO @table (nif, fname, lname, zip, locality, street, [number], birth_date, sex, establishment_number, 
							schedule_id, private_phone, company_phone) 
    VALUES (@nif, @fname, @lname, @zip, @locality, @street, @number, @birth_date, @sex, @establishment_number, 
				@schedule_id, @private_phone, @company_phone)

    RETURN
END
GO


-- UDF to return all of the (specific) details of an effective employee (with validation)

DROP FUNCTION IF EXISTS get_effective_details
GO
CREATE FUNCTION get_effective_details(@emp_num INT)
RETURNS @table TABLE (
	nif						INT				NOT NULL,
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
    private_phone           INT             NOT NULL,
    company_phone           INT             NOT NULL,
    speciality              VARCHAR(20),
    manager                 BIT             NOT NULL
)
AS
BEGIN
	DECLARE @nif INT;
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
    DECLARE @private_phone INT;
    DECLARE @company_phone INT;
    DECLARE @speciality VARCHAR(20);
    DECLARE @manager BIT = 0;
    DECLARE @phone VARCHAR(9);

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

    DECLARE effective_cursor CURSOR FOR 
        SELECT Pessoa.nif, Pnome, Unome, cod_postal, localidade, rua, numero, data_nascimento, sexo, num_estabelecimento, id_horario, especialidade 
        FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif JOIN Efetivo ON Funcionario.nif = Efetivo.nif LEFT JOIN Tem ON Efetivo.nif = nif_efetivo 
        WHERE num_funcionario = @emp_num;

    OPEN effective_cursor;
    FETCH NEXT FROM effective_cursor INTO @nif, @fname, @lname, @zip, @locality, @street, @number, @birth_date, @sex, @establishment_number, @schedule_id, @speciality;
    WHILE @@FETCH_STATUS = 0    -- An effective employee can have multiple specialities
        BEGIN
            INSERT INTO @table (nif, fname, lname, zip, locality, street, [number], birth_date, sex, establishment_number, 
                            schedule_id, private_phone, company_phone, speciality, manager) 
            VALUES (@nif, @fname, @lname, @zip, @locality, @street, @number, @birth_date, @sex, @establishment_number, 
                        @schedule_id, @private_phone, @company_phone, @speciality, @manager)
            FETCH NEXT FROM effective_cursor INTO @nif, @fname, @lname, @zip, @locality, @street, @number, @birth_date, @sex, @establishment_number, @schedule_id, @speciality;
        END
            
    CLOSE effective_cursor;
    DEALLOCATE effective_cursor;

    RETURN
END
GO


-- UDF to return all of the (specific) details of an intern employee (with validation)
DROP FUNCTION IF EXISTS get_intern_details
GO
CREATE FUNCTION get_intern_details(@emp_num INT)
RETURNS @table TABLE (
	nif						INT				NOT NULL,
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
    private_phone           INT             NOT NULL,
    company_phone           INT             NOT NULL,
	internship_end_date		DATE			NOT NULL
)
AS
BEGIN
	DECLARE @nif INT;
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
    DECLARE @private_phone INT;
    DECLARE @company_phone INT;
	DECLARE @internship_end_date DATE;
    DECLARE @phone VARCHAR(9);

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

    DECLARE intern_cursor CURSOR FOR 
        SELECT Pessoa.nif, Pnome, Unome, cod_postal, localidade, rua, numero, data_nascimento, sexo, num_estabelecimento, id_horario, data_fim_estagio
        FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif JOIN Estagiario ON Funcionario.nif = Estagiario.nif 
		WHERE num_funcionario = @emp_num

    OPEN intern_cursor;
    FETCH NEXT FROM intern_cursor INTO @nif, @fname, @lname, @zip, @locality, @street, @number, @birth_date, @sex, @establishment_number, @schedule_id, @internship_end_date;       
    CLOSE intern_cursor;
    DEALLOCATE intern_cursor;
	
	INSERT INTO @table (nif, fname, lname, zip, locality, street, [number], birth_date, sex, establishment_number, 
							schedule_id, private_phone, company_phone, internship_end_date) 
    VALUES (@nif, @fname, @lname, @zip, @locality, @street, @number, @birth_date, @sex, @establishment_number, 
				@schedule_id, @private_phone, @company_phone, @internship_end_date)
    RETURN
END
GO

