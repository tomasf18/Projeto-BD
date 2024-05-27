from typing import List, NamedTuple   
from pyodbc import IntegrityError
from persistence.session import create_connection

class AppointmentSummary(NamedTuple):
    emp_nif: int
    cli_nif: int
    app_date: str
    app_date_requested: str
    client_Fname: str
    client_Lname: str

class AppointmentSummaryClient(NamedTuple):
    emp_nif: int
    cli_nif: int
    app_date: str
    app_date_requested: str
    emp_name: str
    emp_surname: str

class AppointmentDetails(NamedTuple):
    cli_nif: int
    client_Fname: str
    client_Lname: str
    emp_nif: int
    emp_name: str
    emp_surname: str
    service_designation: str
    app_date: str
    app_date_requested: str
    establishment_id: int

def list_appointments_by_acc_emp(func_number: int, order_by: str) -> list[AppointmentSummary]:
    order_by_column = 'Marcacao.nif_cliente' if order_by == 'nif' else 'Marcacao.data_marcacao'
    with create_connection() as conn:
        cursor = conn.cursor()
        nif = cursor.execute(f"SELECT nif FROM Funcionario WHERE num_funcionario = {func_number};").fetchone()[0]
        cursor.execute(f"""
            SELECT Marcacao.*, Pessoa.Pnome, Pessoa.Unome 
            FROM Marcacao 
            JOIN Pessoa ON Marcacao.nif_cliente = Pessoa.nif 
            WHERE Marcacao.nif_funcionario = {nif} 
            ORDER BY {order_by_column};
        """)
        rows = cursor.fetchall()
        cursor.close()

    appointments = []

    for row in rows:
        appointments.append(AppointmentSummary(row.nif_funcionario, row.nif_cliente, row.data_marcacao, row.data_pedido, row.Pnome, row.Unome))

    return appointments

def list_appointments_by_acc_cli(cli_number: int) -> list[AppointmentSummaryClient]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cli_nif = cursor.execute(f"SELECT nif FROM Cliente WHERE num_conta = {cli_number};").fetchone()[0]
        cursor.execute(f"""
            SELECT Marcacao.*, Pessoa.Pnome, Pessoa.Unome 
            FROM Marcacao 
            JOIN Pessoa ON Marcacao.nif_funcionario = Pessoa.nif 
            WHERE Marcacao.nif_cliente = {cli_nif};
        """)
        rows = cursor.fetchall()
        cursor.close()
    
    appointments = []

    for row in rows:
        appointments.append(AppointmentSummaryClient(row.nif_funcionario, row.nif_cliente, row.data_marcacao, row.data_pedido, row.Pnome, row.Unome))
    
    return appointments

def read(nif_emp: int, nif_cli: int, date: str, hour: str) -> AppointmentDetails:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT * FROM get_appointment_details({nif_emp}, {nif_cli}, '{date} {hour}');""")
        rows = cursor.fetchall()
        cursor.close()

    services = [row.designacao_tipo_serv for row in rows]
    row = rows[0]
    return AppointmentDetails(row.nif_cliente, row.client_name, row.client_surname, row.nif_funcionario, row.employee_name, row.employee_surname, services, row.data_marcacao, row.data_pedido, row.num_estabelecimento)
