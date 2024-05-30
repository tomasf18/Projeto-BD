ALTER TABLE Cliente DROP CONSTRAINT FK_Cliente_Pessoa
ALTER TABLE Funcionario DROP CONSTRAINT FK_Funcionario_Pessoa
ALTER TABLE Funcionario DROP CONSTRAINT FK_Funcionario_Horario
ALTER TABLE Funcionario DROP CONSTRAINT FK_Funcionario_Estabelecimento
ALTER TABLE Estabelecimento DROP CONSTRAINT FK_Estabelecimento_Efetivo
ALTER TABLE Efetivo DROP CONSTRAINT FK_Efetivo_Funcionario 
ALTER TABLE Estagiario DROP CONSTRAINT FK_Estagiario_Funcionario 
ALTER TABLE Nums_telem_func DROP CONSTRAINT FK_Nums_telem_func_Funcionario
ALTER TABLE Avaliacao DROP CONSTRAINT FK_Avaliacao_Funcionario
ALTER TABLE Avaliacao DROP CONSTRAINT FK_Avaliacao_Cliente
ALTER TABLE Tem DROP CONSTRAINT FK_Tem_Especialidade 
ALTER TABLE Tem DROP CONSTRAINT FK_Tem_Efetivo 
ALTER TABLE Contrato DROP CONSTRAINT FK_Contrato_Efetivo 
ALTER TABLE Marcacao DROP CONSTRAINT FK_Marcacao_Funcionario 
ALTER TABLE Marcacao DROP CONSTRAINT FK_Marcacao_Cliente
ALTER TABLE Inclui DROP CONSTRAINT FK_Inclui_Marcacao 
ALTER TABLE Inclui DROP CONSTRAINT FK_Inclui_Tipo_servico
ALTER TABLE Servico DROP CONSTRAINT FK_Servico_Tipo_servico
GO
DROP TABLE IF EXISTS Pessoa
DROP TABLE IF EXISTS Cliente
DROP TABLE IF EXISTS Funcionario
DROP TABLE IF EXISTS Horario
DROP TABLE IF EXISTS Estabelecimento
DROP TABLE IF EXISTS Efetivo
DROP TABLE IF EXISTS Especialidade
DROP TABLE IF EXISTS Tem
DROP TABLE IF EXISTS Contrato
DROP TABLE IF EXISTS Estagiario
DROP TABLE IF EXISTS Nums_telem_func
DROP TABLE IF EXISTS Avaliacao
DROP TABLE IF EXISTS Marcacao
DROP TABLE IF EXISTS Tipo_servico
DROP TABLE IF EXISTS Inclui
DROP TABLE IF EXISTS Servico
GO

CREATE TABLE Pessoa (
    Pnome                   VARCHAR(15)             NOT NULL,
    Unome                   VARCHAR(15)             NOT NULL,
    nif                     INT                     NOT NULL,
    cod_postal              VARCHAR(8),
    localidade              VARCHAR(20),
    rua                     VARCHAR(30),
    numero                  INT,
    data_nascimento         DATE                    NOT NULL,
    sexo                    CHAR(1)                 NOT NULL,
    PRIMARY KEY (nif),
    CHECK (nif >= 100000000 AND nif <= 999999999),
    CHECK (LEN(Pnome) > 0),
    CHECK (LEN(Unome) > 0),
    CHECK (cod_postal IS NULL OR LEN(cod_postal) = 8),
    CHECK (localidade IS NULL OR LEN(localidade) > 0),
    CHECK (rua IS NULL OR LEN(rua) > 0),
    CHECK (numero IS NULL OR numero > 0),
    CHECK (data_nascimento < CAST(GETDATE() AS DATE)),
    CHECK (sexo = 'M' OR sexo = 'F')
);


CREATE TABLE Cliente (
    nif                     INT                     NOT NULL,
    num_conta               INT                     NOT NULL,
    num_telemovel           INT,
    PRIMARY KEY (nif),
    UNIQUE (num_conta),
    CHECK (num_conta > 0),
    CHECK (num_telemovel IS NULL OR (num_telemovel >= 900000000 AND num_telemovel <= 999999999))
);


CREATE TABLE Funcionario (
    nif                     INT                     NOT NULL,
    num_funcionario         INT                     NOT NULL,
    num_estabelecimento     INT                     NOT NULL, /* Para ter número de funcionário, tem de trabalhar para um estabelecimento */
    id_horario              INT                     NOT NULL,
    PRIMARY KEY (nif),
    UNIQUE (num_funcionario),
    CHECK (num_funcionario > 0),
    CHECK (num_estabelecimento > 0)
);


CREATE TABLE Horario (
    id                      INT                     NOT NULL,
    dia_folga               VARCHAR(13)             NOT NULL, 
    h_entrada               TIME                    NOT NULL,
    h_saida                 TIME                    NOT NULL,
    PRIMARY KEY (id),
    CHECK (id > 0),
    CHECK (dia_folga = 'Segunda-feira' OR dia_folga = 'Terça-feira' OR dia_folga = 'Quarta-feira' OR dia_folga = 'Quinta-feira' OR dia_folga = 'Sexta-feira' OR dia_folga = 'Sábado' OR dia_folga = 'Domingo'),
    CHECK (h_entrada < h_saida),
    CHECK (h_entrada >= '00:00:00' AND h_entrada <= '23:59:59'),
    CHECK (h_saida >= '00:00:00' AND h_saida <= '23:59:59')
);


CREATE TABLE Estabelecimento (
    id                      INT                     NOT NULL,
    especificacao           VARCHAR(12)             NOT NULL,
    cod_postal              VARCHAR(8)              NOT NULL,
    localidade              VARCHAR(20)             NOT NULL,
    rua                     VARCHAR(30)             NOT NULL,
    numero                  INT                     NOT NULL,
    nif_gerente             INT                     NOT NULL,
    data_inicio_gerente     DATE                    NOT NULL,
    PRIMARY KEY (id),
    CHECK (id > 0),
    CHECK (especificacao = 'Cabeleireiro' OR especificacao = 'Barbeiro'),
    CHECK (LEN(cod_postal) = 8),
    CHECK (LEN(localidade) > 0),
    CHECK (LEN(rua) > 0),
    CHECK (numero > 0),
    CHECK (data_inicio_gerente < CAST(GETDATE() AS DATE))
);


CREATE TABLE Efetivo (
    nif                     INT                     NOT NULL,
    PRIMARY KEY (nif)
);


CREATE TABLE Especialidade (
    designacao             VARCHAR(20)             NOT NULL,
    PRIMARY KEY (designacao),
    CHECK (LEN(designacao) > 0)
);


CREATE TABLE Tem (
    nif_efetivo             INT                     NOT NULL,
    especialidade           VARCHAR(20)             NOT NULL,
    PRIMARY KEY (nif_efetivo, especialidade)
);


CREATE TABLE Contrato (
    nif_efetivo             INT                     NOT NULL,
    salario                 DECIMAL(10,2)           NOT NULL,
    descricao               VARCHAR(100)            NOT NULL,
    data_inicio             DATE                    NOT NULL,
    data_fim                DATE                    NOT NULL,
    PRIMARY KEY (nif_efetivo),
    CHECK (salario > 0), 
    CHECK (LEN(descricao) > 0),
    CHECK (data_inicio < data_fim)
);


CREATE TABLE Estagiario (
    nif                     INT                     NOT NULL,
    data_fim_estagio        DATE                    NOT NULL,
    PRIMARY KEY (nif)
);


CREATE TABLE Nums_telem_func (
    nif_func                INT                     NOT NULL,
    num_telem               INT                     NOT NULL,
    PRIMARY KEY (nif_func, num_telem),
    CHECK (num_telem >= 000000000 AND num_telem <= 999999999)
);


CREATE TABLE Avaliacao (
    nif_funcionario         INT                     NOT NULL,
    nif_cliente             INT                     NOT NULL,
    data_avaliacao          DATETIME                NOT NULL,
    n_estrelas              INT                     NOT NULL,
    comentario              VARCHAR(100),
    PRIMARY KEY (nif_funcionario, nif_cliente, data_avaliacao),
    CHECK (data_avaliacao <= CAST(GETDATE() AS DATE)),
    CHECK (n_estrelas >= 1 AND n_estrelas <= 5)
);


CREATE TABLE Marcacao (
    nif_funcionario         INT                     NOT NULL,
    nif_cliente             INT                     NOT NULL,
    data_marcacao           DATETIME                NOT NULL,
    data_pedido             DATETIME                NOT NULL,
    PRIMARY KEY (nif_funcionario, nif_cliente, data_marcacao),
    CHECK (data_pedido <= GETDATE())
);


CREATE TABLE Tipo_servico (
    sexo                    CHAR(1)                 NOT NULL,
    designacao              VARCHAR(30)             NOT NULL,
    PRIMARY KEY (sexo, designacao),
    CHECK (sexo = 'M' OR sexo = 'F'),
    CHECK (LEN(designacao) > 0)
);


CREATE TABLE Inclui (
    data_marcacao           DATETIME                NOT NULL,
    nif_funcionario         INT                     NOT NULL,
    nif_cliente             INT                     NOT NULL,
    sexo                    CHAR(1)                 NOT NULL,
    designacao_tipo_serv    VARCHAR(30)             NOT NULL,
    PRIMARY KEY (nif_funcionario, nif_cliente, data_marcacao, sexo, designacao_tipo_serv)
);


CREATE TABLE Servico (
    nome                   VARCHAR(30)             NOT NULL,
    preco                  DECIMAL(10,2)           NOT NULL,
    sexo                   CHAR(1)                 NOT NULL,
    designacao             VARCHAR(30)             NOT NULL,
    PRIMARY KEY (nome, sexo, designacao),
    CHECK (LEN(nome) > 0),
    CHECK (preco > 0)
);



/* FK Constraints */

ALTER TABLE Cliente 
    ADD CONSTRAINT FK_Cliente_Pessoa FOREIGN KEY (nif) REFERENCES Pessoa(nif);

ALTER TABLE Funcionario 
    ADD CONSTRAINT FK_Funcionario_Pessoa FOREIGN KEY (nif) REFERENCES Pessoa(nif);

-- Done
ALTER TABLE Funcionario 
    ADD CONSTRAINT FK_Funcionario_Horario FOREIGN KEY (id_horario) REFERENCES Horario(id);
    -- ON DELETE RESTRICT /* TRIGGER INSTEAD OF que atribui um novo horário ao funcionário antes do antigo ser eliminado (se possível) */


ALTER TABLE Funcionario
    ADD CONSTRAINT FK_Funcionario_Estabelecimento FOREIGN KEY (num_estabelecimento) REFERENCES Estabelecimento(id);
    -- ON DELETE CASCADE /* Criar trigger para eliminar as pessoas que trabalhavam naquele estabelecimento */


-- Done
ALTER TABLE Estabelecimento 
    ADD CONSTRAINT FK_Estabelecimento_Efetivo FOREIGN KEY (nif_gerente) REFERENCES Efetivo(nif);
    -- ON DELETE RESTRICT -> TRIGGER INSTEAD OF que atribui um novo gerente ao estabelecimento antes do antigo ser eliminado (se possível) */

ALTER TABLE Efetivo 
    ADD CONSTRAINT FK_Efetivo_Funcionario FOREIGN KEY (nif) REFERENCES Funcionario(nif);

ALTER TABLE Estagiario 
    ADD CONSTRAINT FK_Estagiario_Funcionario FOREIGN KEY (nif) REFERENCES Funcionario(nif);

ALTER TABLE Nums_telem_func 
    ADD CONSTRAINT FK_Nums_telem_func_Funcionario FOREIGN KEY (nif_func) REFERENCES Funcionario(nif);

ALTER TABLE Avaliacao 
    ADD CONSTRAINT FK_Avaliacao_Funcionario FOREIGN KEY (nif_funcionario) REFERENCES Funcionario(nif);

ALTER TABLE Avaliacao 
    ADD CONSTRAINT FK_Avaliacao_Cliente FOREIGN KEY (nif_cliente) REFERENCES Cliente(nif); /* Se um cliente for eliminado, todas as avaliações feitas por esse cliente também serão eliminadas */

ALTER TABLE Tem 
    ADD CONSTRAINT FK_Tem_Especialidade FOREIGN KEY (especialidade) REFERENCES Especialidade(designacao)
    ON DELETE CASCADE;  /* Se uma especialidade for eliminada, o registo Tem que liga um efetivo à especialidde é eliminado também */


ALTER TABLE Tem 
    ADD CONSTRAINT FK_Tem_Efetivo FOREIGN KEY (nif_efetivo) REFERENCES Efetivo(nif);

ALTER TABLE Contrato
    ADD CONSTRAINT FK_Contrato_Efetivo FOREIGN KEY (nif_efetivo) REFERENCES Efetivo(nif);

ALTER TABLE Marcacao 
    ADD CONSTRAINT FK_Marcacao_Funcionario FOREIGN KEY (nif_funcionario) REFERENCES Funcionario(nif);

ALTER TABLE Marcacao 
    ADD CONSTRAINT FK_Marcacao_Cliente FOREIGN KEY (nif_cliente) REFERENCES Cliente(nif);

ALTER TABLE Inclui 
    ADD CONSTRAINT FK_Inclui_Marcacao FOREIGN KEY (nif_funcionario, nif_cliente, data_marcacao) REFERENCES Marcacao(nif_funcionario, nif_cliente, data_marcacao);

ALTER TABLE Inclui
    ADD CONSTRAINT FK_Inclui_Tipo_servico FOREIGN KEY (sexo, designacao_tipo_serv) REFERENCES Tipo_servico(sexo, designacao);

ALTER TABLE Servico 
    ADD CONSTRAINT FK_Servico_Tipo_servico FOREIGN KEY (sexo, designacao) REFERENCES Tipo_servico(sexo, designacao)
    ON DELETE CASCADE;