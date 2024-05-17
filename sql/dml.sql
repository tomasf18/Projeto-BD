INSERT INTO Horario (id, dia_folga, h_entrada, h_saida) VALUES
(1, 'Segunda-feira', '08:00:00', '17:00:00'),
(2, 'Segunda-feira', '13:00:00', '20:00:00'),
(3, 'Terça-feira', '08:00:00', '17:00:00'),
(4, 'Terça-feira', '13:00:00', '20:00:00'),
(5, 'Quarta-feira', '08:00:00', '17:00:00'),
(6, 'Quarta-feira', '13:00:00', '20:00:00'),
(7, 'Quinta-feira', '08:00:00', '17:00:00'),
(8, 'Quinta-feira', '13:00:00', '20:00:00'),
(9, 'Sexta-feira', '08:00:00', '17:00:00'),
(10, 'Sexta-feira', '13:00:00', '20:00:00'),
(11, 'Sábado', '08:00:00', '17:00:00'),
(12, 'Sábado', '13:00:00', '20:00:00'),
(13, 'Domingo', '08:00:00', '17:00:00'),
(14, 'Domingo', '13:00:00', '20:00:00');


ALTER TABLE Estabelecimento
    ALTER COLUMN nif_gerente INT NULL;
ALTER TABLE Estabelecimento
    ALTER COLUMN data_inicio_gerente DATE NULL;

INSERT INTO Estabelecimento(id, especificacao, cod_postal, localidade, rua, numero, nif_gerente, data_inicio_gerente) VALUES
(1, 'Cabeleireiro', '3810-880', 'Oliveirinha', 'Rua 1º de Maio', 3, NULL, NULL),
(2, 'Barbeiro', '4100-367', 'Ramalde', 'Rua O 1º de Janeiro', 30, NULL, NULL),
(3, 'Barbeiro', '2655-319', 'Ericeira', 'Rua 1º de Maio', 56, NULL, NULL),
(4, 'Cabeleireiro', '1000-001', 'Lisboa', 'Avenida da Liberdade', 123, NULL, NULL),
(5, 'Barbeiro', '4050-123', 'Porto', 'Rua das Flores', 45, NULL, NULL),
(6, 'Barbeiro', '3800-420', 'Aveiro', 'Rua da Liberdade', 7, NULL, NULL),
(7, 'Barbeiro', '4000-789', 'Porto', 'Avenida Boavista', 88, NULL, NULL),
(8, 'Cabeleireiro', '4100-222', 'Porto', 'Rua da Boémia', 22, NULL, NULL);

INSERT INTO Pessoa(Pnome, Unome, nif, cod_postal, localidade, rua, numero, data_nascimento, sexo) VALUES
('João', 'Silva', 238475910, '3810-880', 'Oliveirinha', 'Rua 1º de Maio', 10, '1990-01-01', 'M'),
('Miguel', 'Santos', 645892314, '3810-880', 'Oliveirinha', 'Rua O 1º de Maio', 15, '1995-03-12', 'M'),
('Maria', 'Fernandes', 784231096, '2655-319', 'Ericeira', 'Rua 1º de Maio', 56, '1993-03-03', 'F'),
('Maria', 'Santos', 539287461, '4100-367', 'Ramalde', 'Rua O 1º de Janeiro', 30, '1995-02-02', 'F'),
('Manuel', 'Fernandes', 102938475, '2655-319', 'Ericeira', 'Rua 1º de Maio', 56, '1993-03-03', 'M'),
('Ana', 'Ferreira', 382910485, '1500-001', 'Lisboa', 'Avenida da Liberdade', 20, '1988-06-15', 'F'),
('Bruno', 'Martins', 657894321, '4100-002', 'Porto', 'Rua das Flores', 40, '1992-09-20', 'M'),
('Carla', 'Rodrigues', 213456789, '2655-003', 'Ericeira', 'Rua das Rosas', 8, '1997-04-30', 'F'),
('Daniel', 'Oliveira', 876543210, '1000-004', 'Lisboa', 'Avenida do Mar', 30, '1990-11-10', 'M'),
('Eva', 'Sousa', 109283746, '4100-005', 'Porto', 'Rua do Castelo', 25, '1985-03-25', 'F'),
('Filipe', 'Almeida', 827364591, '1500-006', 'Lisboa', 'Avenida da Liberdade', 50, '1993-08-12', 'M'),
('Gabriela', 'Pereira', 204819673, '4100-007', 'Porto', 'Rua da Boavista', 60, '1987-12-18', 'F'),
('Hugo', 'Silveira', 638172945, '2655-008', 'Ericeira', 'Rua do Sol', 12, '1996-05-22', 'M'),
('Inês', 'Costa', 495867213, '1500-009', 'Lisboa', 'Avenida das Flores', 35, '1994-02-05', 'F'),
('Joana', 'Mendes', 925638471, '4100-010', 'Porto', 'Rua do Mar', 22, '1989-10-08', 'F'),
('Kevin', 'Ramos', 374691825, '2655-011', 'Ericeira', 'Rua do Mar', 45, '1991-07-17', 'M'),
('Laura', 'Teixeira', 638127394, '1500-012', 'Lisboa', 'Rua do Sol', 18, '1998-11-29', 'F'),
('Mário', 'Lopes', 927364185, '4100-013', 'Porto', 'Rua das Gaivotas', 27, '1986-09-03', 'M'),
('Núria', 'Ferreira', 275931468, '2655-014', 'Ericeira', 'Rua do Castelo', 10, '1995-12-14', 'F'),
('Paulo', 'Gomes', 384619725, '1500-015', 'Lisboa', 'Avenida das Palmeiras', 55, '1997-03-08', 'M'),
('Raquel', 'Alves', 928374156, '4100-016', 'Porto', 'Rua da Liberdade', 32, '1990-04-20', 'F'),
('Sofia', 'Pires', 736491825, '2655-017', 'Ericeira', 'Rua das Oliveiras', 9, '1988-08-27', 'F'),
('Tiago', 'Carvalho', 182736495, '1500-018', 'Lisboa', 'Avenida do Mar', 48, '1993-06-03', 'M'),
('Vanessa', 'Sousa', 839274651, '4100-019', 'Porto', 'Rua do Sol', 17, '1996-01-12', 'F'),
('Xavier', 'Fernandes', 527364891, '2655-020', 'Ericeira', 'Rua do Mar', 23, '1998-09-05', 'M'),
('Yara', 'Machado', 748192536, '1500-021', 'Lisboa', 'Avenida das Gaivotas', 33, '1991-05-18', 'F'),
('Zé', 'Oliveira', 485729163, '4100-022', 'Porto', 'Rua das Palmeiras', 28, '1987-07-31', 'M'),
('Ingrid', 'Santos', 679183254, '2655-023', 'Ericeira', 'Rua das Oliveiras', 16, '1994-02-14', 'F'),
('Luís', 'Martins', 918273645, '1500-024', 'Lisboa', 'Avenida da Liberdade', 42, '1986-12-20', 'M'),
('Ana', 'Santos', 538194627, '4100-025', 'Porto', 'Rua das Gaivotas', 14, '1993-08-22', 'F'),
('Pedro', 'Silva', 825719364, '2655-026', 'Ericeira', 'Rua das Palmeiras', 26, '1990-10-15', 'M'),
('Mariana', 'Fernandes', 371928546, '1500-027', 'Lisboa', 'Avenida do Mar', 37, '1987-05-07', 'F'),
('Ricardo', 'Pereira', 917284563, '4100-028', 'Porto', 'Rua do Sol', 21, '1995-02-28', 'M'),
('Catarina', 'Oliveira', 649182735, '2655-029', 'Ericeira', 'Rua das Oliveiras', 38, '1992-09-09', 'F'),
('André', 'Martins', 728361954, '1500-030', 'Lisboa', 'Avenida da Liberdade', 19, '1989-03-16', 'M'),
('Carolina', 'Rodrigues', 819473625, '4100-031', 'Porto', 'Rua do Mar', 31, '1996-07-11', 'F'),
('Gonçalo', 'Sousa', 375926184, '2655-032', 'Ericeira', 'Rua das Gaivotas', 43, '1994-01-04', 'M'),
('Inês', 'Ferreira', 619482753, '1500-033', 'Lisboa', 'Avenida das Palmeiras', 29, '1991-12-19', 'F'),
('Diogo', 'Carvalho', 927364815, '4100-034', 'Porto', 'Rua das Flores', 24, '1988-04-02', 'M');

INSERT INTO Funcionario(nif, num_funcionario, num_estabelecimento, id_horario) VALUES
(238475910, 1, 1, 1), -- João Silva no Estabelecimento 1
(645892314, 2, 1, 2), -- Miguel Santos no Estabelecimento 1
(784231096, 3, 1, 3), -- Maria Fernandes no Estabelecimento 1
(539287461, 4, 2, 4), -- Maria Santos no Estabelecimento 2
(102938475, 5, 3, 5), -- Manuel Fernandes no Estabelecimento 3
(382910485, 6, 4, 6), -- Ana Ferreira no Estabelecimento 4
(657894321, 7, 5, 7), -- Bruno Martins no Estabelecimento 5
(213456789, 8, 6, 8), -- Carla Rodrigues no Estabelecimento 6
(876543210, 9, 7, 9), -- Daniel Oliveira no Estabelecimento 7
(109283746, 10, 8, 10), -- Eva Sousa no Estabelecimento 8
(827364591, 11, 1, 11), -- Filipe Almeida no Estabelecimento 1
(204819673, 12, 2, 12), -- Gabriela Pereira no Estabelecimento 2
(638172945, 13, 3, 13), -- Hugo Silveira no Estabelecimento 3
(495867213, 14, 4, 14), -- Inês Costa no Estabelecimento 4
(925638471, 15, 5, 1), -- Joana Mendes no Estabelecimento 5
(374691825, 16, 6, 2), -- Kevin Ramos no Estabelecimento 6
(638127394, 17, 7, 3), -- Laura Teixeira no Estabelecimento 7
(927364185, 18, 8, 4), -- Mário Lopes no Estabelecimento 8
(275931468, 19, 1, 5), -- Núria Ferreira no Estabelecimento 1
(384619725, 20, 2, 6), -- Paulo Gomes no Estabelecimento 2
(928374156, 21, 3, 7), -- Raquel Alves no Estabelecimento 3
(736491825, 22, 4, 8), -- Sofia Pires no Estabelecimento 4
(182736495, 23, 5, 9), -- Tiago Carvalho no Estabelecimento 5
(839274651, 24, 6, 10), -- Vanessa Sousa no Estabelecimento 6
(527364891, 25, 7, 11); -- Xavier Fernandes no Estabelecimento 7

INSERT INTO Cliente(nif, num_conta, num_telemovel) VALUES
(538194627, 123456789, 912345678), -- Ana Santos
(825719364, 234567890, 923456789), -- Pedro Silva
(371928546, 345678901, 934567890), -- Mariana Fernandes
(917284563, 456789012, 945678901), -- Ricardo Pereira
(649182735, 567890123, 956789012), -- Catarina Oliveira
(728361954, 678901234, 967890123), -- André Martins
(819473625, 789012345, 978901234), -- Carolina Rodrigues
(375926184, 890123456, 989012345), -- Gonçalo Sousa
(619482753, 901234567, 991234567), -- Inês Ferreira
(927364815, 012345678, 992345678), -- Diogo Carvalho
(679183254, 112345678, 993456789), -- Ingrid Santos
(918273645, 223456789, 994567890); -- Luís Martins

INSERT INTO Efetivo(nif) VALUES
(238475910), -- João Silva
(645892314), -- Miguel Santos
(784231096), -- Maria Fernandes
(539287461), -- Maria Santos
(102938475), -- Manuel Fernandes
(382910485), -- Ana Ferreira
(657894321), -- Bruno Martins
(213456789), -- Carla Rodrigues
(876543210), -- Daniel Oliveira
(109283746), -- Eva Sousa
(827364591), -- Filipe Almeida
(204819673), -- Gabriela Pereira
(638172945), -- Hugo Silveira
(495867213), -- Inês Costa
(925638471), -- Joana Mendes
(374691825), -- Kevin Ramos
(638127394), -- Laura Teixeira
(927364185), -- Mário Lopes
(275931468), -- Núria Ferreira
(384619725); -- Paulo Gomes

-- Inserção de estagiários
INSERT INTO Estagiario(nif, data_fim_estagio) VALUES
(928374156, '2024-06-30'), -- Raquel Alves
(736491825, '2024-06-30'), -- Sofia Pires
(182736495, '2024-06-30'), -- Tiago Carvalho
(839274651, '2024-06-30'), -- Vanessa Sousa
(527364891, '2024-06-30'); -- Xavier Fernandes


UPDATE Estabelecimento
SET nif_gerente = 238475910, data_inicio_gerente = '2019-01-01' -- João Silva gere o Estabelecimento 1
WHERE id = 1;

UPDATE Estabelecimento
SET nif_gerente = 539287461, data_inicio_gerente = '2020-03-01' -- Maria Santos gere o Estabelecimento 2
WHERE id = 2;

UPDATE Estabelecimento
SET nif_gerente = 102938475, data_inicio_gerente = '2021-05-01' -- Manuel Fernandes gere o Estabelecimento 3
WHERE id = 3;

UPDATE Estabelecimento
SET nif_gerente = 382910485, data_inicio_gerente = '2022-07-01' -- Ana Ferreira gere o Estabelecimento 4
WHERE id = 4;

UPDATE Estabelecimento
SET nif_gerente = 657894321, data_inicio_gerente = '2023-09-01' -- Bruno Martins gere o Estabelecimento 5
WHERE id = 5;

UPDATE Estabelecimento
SET nif_gerente = 213456789, data_inicio_gerente = '2021-11-01' -- Carla Rodrigues gere o Estabelecimento 6
WHERE id = 6;

UPDATE Estabelecimento
SET nif_gerente = 876543210, data_inicio_gerente = '2023-01-01' -- Daniel Oliveira gere o Estabelecimento 7
WHERE id = 7;

UPDATE Estabelecimento
SET nif_gerente = 109283746, data_inicio_gerente = '2022-03-01' -- Eva Sousa gere o Estabelecimento 8
WHERE id = 8;

INSERT INTO Especialidade(designacao) VALUES
('Corte de Cabelo'),
('Barba'),
('Coloração'),
('Madeixas'),
('Tratamento Capilar'),
('Tratamento Facial');

INSERT INTO Tem(nif_efetivo, especialidade) VALUES
(238475910, 'Corte de Cabelo'), -- João Silva
(238475910, 'Barba'), -- João Silva
(645892314, 'Corte de Cabelo'), -- Miguel Santos
(784231096, 'Coloração'), -- Maria Fernandes
(784231096, 'Madeixas'), -- Maria Fernandes
(539287461, 'Corte de Cabelo'), -- Maria Santos
(539287461, 'Tratamento Facial'), -- Maria Santos
(102938475, 'Corte de Cabelo'), -- Manuel Fernandes
(102938475, 'Barba'), -- Manuel Fernandes
(102938475, 'Coloração'), -- Manuel Fernandes
(382910485, 'Corte de Cabelo'), -- Ana Ferreira
(382910485, 'Tratamento Capilar'), -- Ana Ferreira
(657894321, 'Corte de Cabelo'), -- Bruno Martins
(657894321, 'Barba'), -- Bruno Martins
(657894321, 'Tratamento Capilar'), -- Bruno Martins
(213456789, 'Corte de Cabelo'), -- Carla Rodrigues
(213456789, 'Tratamento Facial'), -- Carla Rodrigues
(876543210, 'Barba'), -- Daniel Oliveira
(109283746, 'Corte de Cabelo'), -- Eva Sousa
(109283746, 'Coloração'), -- Eva Sousa
(109283746, 'Madeixas'), -- Eva Sousa
(109283746, 'Tratamento Facial'); -- Eva Sousa

INSERT INTO Contrato(nif_efetivo, salario, descricao, data_inicio, data_fim) VALUES
(238475910, 1000.00, 'Contrato de trabalho de João Silva', '2020-03-15', '2023-03-14'), -- João Silva
(645892314, 1000.00, 'Contrato de trabalho de Miguel Santos', '2020-05-20', '2023-05-19'), -- Miguel Santos
(784231096, 1000.00, 'Contrato de trabalho de Maria Fernandes', '2020-07-25', '2023-07-24'), -- Maria Fernandes
(539287461, 1000.00, 'Contrato de trabalho de Maria Santos', '2020-09-30', '2023-09-29'), -- Maria Santos
(102938475, 1000.00, 'Contrato de trabalho de Manuel Fernandes', '2021-01-05', '2024-01-04'), -- Manuel Fernandes
(382910485, 1000.00, 'Contrato de trabalho de Ana Ferreira', '2021-03-10', '2024-03-09'), -- Ana Ferreira
(657894321, 1000.00, 'Contrato de trabalho de Bruno Martins', '2021-05-15', '2024-05-14'), -- Bruno Martins
(213456789, 1000.00, 'Contrato de trabalho de Carla Rodrigues', '2021-07-20', '2024-07-19'), -- Carla Rodrigues
(876543210, 1000.00, 'Contrato de trabalho de Daniel Oliveira', '2021-09-25', '2024-09-24'), -- Daniel Oliveira
(109283746, 1000.00, 'Contrato de trabalho de Eva Sousa', '2022-11-01', '2025-10-31'), -- Eva Sousa
(827364591, 1000.00, 'Contrato de trabalho de Filipe Almeida', '2023-01-15', '2026-01-14'), -- Filipe Almeida
(204819673, 1000.00, 'Contrato de trabalho de Gabriela Pereira', '2023-03-20', '2026-03-19'), -- Gabriela Pereira
(638172945, 1000.00, 'Contrato de trabalho de Hugo Silveira', '2023-05-25', '2026-05-24'), -- Hugo Silveira
(495867213, 1000.00, 'Contrato de trabalho de Inês Costa', '2023-07-30', '2026-07-29'), -- Inês Costa
(925638471, 1000.00, 'Contrato de trabalho de Joana Mendes', '2023-09-04', '2026-09-03'), -- Joana Mendes
(374691825, 1000.00, 'Contrato de trabalho de Kevin Ramos', '2023-11-09', '2026-11-08'), -- Kevin Ramos
(638127394, 1000.00, 'Contrato de trabalho de Laura Teixeira', '2024-01-14', '2027-01-13'), -- Laura Teixeira
(927364185, 1000.00, 'Contrato de trabalho de Mário Lopes', '2024-03-19', '2027-03-18'), -- Mário Lopes
(275931468, 1000.00, 'Contrato de trabalho de Núria Ferreira', '2024-05-24', '2027-05-23'), -- Núria Ferreira
(384619725, 1000.00, 'Contrato de trabalho de Paulo Gomes', '2024-07-29', '2027-07-28'); -- Paulo Gomes

INSERT INTO Nums_telem_func(nif_func, num_telem) VALUES
(238475910, '912345678'), -- João Silva
(238475910, '234123456'), -- João Silva (Empresa)
(645892314, '913456789'), -- Miguel Santos
(645892314, '234234567'), -- Miguel Santos (Empresa)
(784231096, '914567890'), -- Maria Fernandes
(784231096, '234345678'), -- Maria Fernandes (Empresa)
(539287461, '915678901'), -- Maria Santos
(539287461, '234456789'), -- Maria Santos (Empresa)
(102938475, '916789012'), -- Manuel Fernandes
(102938475, '234567890'), -- Manuel Fernandes (Empresa)
(382910485, '917890123'), -- Ana Ferreira
(382910485, '234678901'), -- Ana Ferreira (Empresa)
(657894321, '918901234'), -- Bruno Martins
(657894321, '234789012'), -- Bruno Martins (Empresa)
(213456789, '919012345'), -- Carla Rodrigues
(213456789, '234890123'), -- Carla Rodrigues (Empresa)
(876543210, '920123456'), -- Daniel Oliveira
(876543210, '234901234'), -- Daniel Oliveira (Empresa)
(109283746, '921234567'), -- Eva Sousa
(109283746, '234012345'), -- Eva Sousa (Empresa)
(827364591, '922345678'), -- Filipe Almeida
(827364591, '234112345'), -- Filipe Almeida (Empresa)
(204819673, '923456789'), -- Gabriela Pereira
(204819673, '234223456'), -- Gabriela Pereira (Empresa)
(638172945, '924567890'), -- Hugo Silveira
(638172945, '234334567'), -- Hugo Silveira (Empresa)
(495867213, '925678901'), -- Inês Costa
(495867213, '234445678'), -- Inês Costa (Empresa)
(925638471, '926789012'), -- Joana Mendes
(925638471, '234556789'), -- Joana Mendes (Empresa)
(374691825, '927890123'), -- Kevin Ramos
(374691825, '234667890'), -- Kevin Ramos (Empresa)
(638127394, '928901234'), -- Laura Teixeira
(638127394, '234778901'), -- Laura Teixeira (Empresa)
(927364185, '929012345'), -- Mário Lopes
(927364185, '234889012'), -- Mário Lopes (Empresa)
(275931468, '930123456'), -- Núria Ferreira
(275931468, '234990123'), -- Núria Ferreira (Empresa)
(384619725, '931234567'), -- Paulo Gomes
(384619725, '234101234'), -- Paulo Gomes (Empresa)
(928374156, '932345678'), -- Raquel Alves
(928374156, '234211234'), -- Raquel Alves (Empresa)
(736491825, '933456789'), -- Sofia Pires
(736491825, '234322345'), -- Sofia Pires (Empresa)
(182736495, '934567890'), -- Tiago Carvalho
(182736495, '234433456'), -- Tiago Carvalho (Empresa)
(839274651, '935678901'), -- Vanessa Sousa
(839274651, '234544567'), -- Vanessa Sousa (Empresa)
(527364891, '936789012'), -- Xavier Fernandes
(527364891, '234655678'); -- Xavier Fernandes (Empresa)

INSERT INTO Avaliacao(nif_funcionario, nif_cliente, data_avaliacao, n_estrelas, comentario) VALUES
(238475910, 538194627, '2024-04-22', 5, NULL), -- Ana Santos
(238475910, 825719364, '2024-04-15', 4, 'Serviço de qualidade, mas cheguei à hora da marcação e tive de esperar 15 minutos'), -- Pedro Silva
(238475910, 371928546, '2023-09-10', 5, 'Empregado excelente!'), -- Mariana Fernandes
(238475910, 918273645, '2024-02-19', 3, NULL); -- Luís Martins