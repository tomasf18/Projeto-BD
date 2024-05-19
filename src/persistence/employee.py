from dataclasses import dataclass
from typing import NamedTuple   
from pyodbc import IntegrityError
from persistence import person
from persistence.person import PersonDetails
from persistence.session import create_connection


class EmployeeSummary(NamedTuple):
    employee_number: int
    fname: str
    lname: str

@dataclass
class EmployeeDetails(PersonDetails):
    establishment_number: int
    schedule_id: int


def list_employees() -> list[EmployeeSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT num_funcionario, Pnome, Unome FROM Funcionario JOIN Pessoa ON Funcionario.nif = Pessoa.nif;")
        rows = cursor.fetchall()
        cursor.close()

    employees = []

    for row in rows:
        employees.append(EmployeeSummary(row.num_funcionario, row.Pnome, row.Unome))

    return employees


def list_employees_by_name(name: str) -> list[EmployeeSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT num_funcionario, Pnome, Unome FROM Funcionario JOIN Pessoa ON Funcionario.nif = Pessoa.nif WHERE Pnome + ' ' + Unome LIKE '%{name}%';")
        rows = cursor.fetchall()
        cursor.close()

    employees = []

    for row in rows:
        employees.append(EmployeeSummary(row.num_funcionario, row.Pnome, row.Unome))

    return employees


def read(emp_num: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Funcionario JOIN Pessoa ON Funcionario.nif = Pessoa.nif WHERE Funcionario.num_funcionario = ?;", emp_num)
        row = cursor.fetchone()

    return row.nif, row.num_funcionario, EmployeeDetails(
        fname=row.Pnome,
        lname=row.Unome,
        zip=row.cod_postal or "",
        locality=row.localidade or "",
        street=row.rua or "",
        number=row.numero or "",
        birth_date=row.data_nascimento,
        sex=row.sexo,
        establishment_number=row.num_estabelecimento,
        schedule_id=row.id_horario
    )


def create(nif: int, employee: EmployeeDetails):
    person.create(nif, PersonDetails(employee.fname, employee.lname, employee.zip, employee.locality, employee.street, employee.number, employee.birth_date, employee.sex))  # create person first
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(num_funcionario) FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif JOIN Efetivo ON Funcionario.nif = Efetivo.nif")
        last_emp_row = cursor.fetchone()
        last_emp_num = last_emp_row[0]
        new_emp_num = last_emp_num + 1
        try:
            cursor.execute(
                "INSERT INTO Funcionario (nif, num_funcionario, num_estabelecimento, id_horario) VALUES (?, ?, ?, ?);",
                nif,
                new_emp_num,
                employee.establishment_number,
                employee.schedule_id
            )
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not create employee. Data integrity issue.") from e


def update(nif: int, employee: EmployeeDetails):
    person.update(nif, PersonDetails(employee.fname, employee.lname, employee.zip, employee.locality, employee.street, employee.number, employee.birth_date, employee.sex))  # update person first
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE Funcionario 
                SET num_estabelecimento = ?, id_horario = ?
                WHERE nif = ?;
                """,
                employee.establishment_number,
                employee.schedule_id,
                nif
            )
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not update employee {nif}. Data integrity issue.") from e


def delete(nif: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Funcionario WHERE nif = ?;", nif)
            conn.commit()
            person.delete(nif)  # delete person after
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not delete employee {nif}. Data integrity issue.") from e