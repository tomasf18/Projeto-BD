
-- Delete views

DROP VIEW IF EXISTS viewAppointmentDetails;
GO
-- Create views

CREATE VIEW viewAppointmentDetails AS
SELECT 
    Marcacao.nif_cliente, 
    PessoaCliente.Pnome AS client_name, 
    PessoaCliente.Unome AS client_surname, 
    Marcacao.nif_funcionario, 
    PessoaFuncionario.Pnome AS employee_name, 
    PessoaFuncionario.Unome AS employee_surname, 
    Inclui.designacao_tipo_serv, 
    Marcacao.data_marcacao, 
    Marcacao.data_pedido, 
    Funcionario.num_estabelecimento
FROM Marcacao   
JOIN Pessoa AS PessoaCliente ON Marcacao.nif_cliente = PessoaCliente.nif 
JOIN Pessoa AS PessoaFuncionario ON Marcacao.nif_funcionario = PessoaFuncionario.nif 
JOIN Funcionario ON Marcacao.nif_funcionario = Funcionario.nif
JOIN Inclui ON Marcacao.nif_funcionario = Inclui.nif_funcionario
    AND Marcacao.nif_cliente = Inclui.nif_cliente 
    AND Marcacao.data_marcacao = Inclui.data_marcacao
GO

