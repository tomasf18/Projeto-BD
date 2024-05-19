from dataclasses import dataclass
from typing import NamedTuple
from pyodbc import IntegrityError
from persistence import employee
from persistence.employee import EmployeeDetails
from persistence.session import create_connection


class InternSummary(NamedTuple):
    employee_number: int
    fname: str
    lname: str
    type: str = "I"

@dataclass
class InternDetails(EmployeeDetails):
    internship_end_date: str  # Assuming the date is stored as a string in YYYY-MM-DD format


def list_interns() -> list[InternSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT num_funcionario, Pnome, Unome FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif JOIN Estagiario ON Funcionario.nif = Estagiario.nif")
        rows = cursor.fetchall()
        cursor.close()

    interns = []

    for row in rows:
        interns.append(InternSummary(row.num_funcionario, row.Pnome, row.Unome))

    return interns


def list_interns_by_name(name: str) -> list[InternSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT num_funcionario, Pnome, Unome FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif JOIN Estagiario ON Funcionario.nif = Estagiario.nif WHERE Pnome + ' ' + Unome LIKE '%{name}%';")
        rows = cursor.fetchall()
        cursor.close()

    interns = []

    for row in rows:
        interns.append(InternSummary(row.num_funcionario, row.Pnome, row.Unome))

    return interns


def read(emp_num: int) -> InternDetails:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif JOIN Estagiario ON Funcionario.nif = Estagiario.nif WHERE num_funcionario = ?;", emp_num)
        row = cursor.fetchone()

    return row.nif, row.num_funcionario, InternDetails(
        fname=row.Pnome,
        lname=row.Unome,
        zip=row.cod_postal or "",
        locality=row.localidade or "",
        street=row.rua or "",
        number=row.numero or "",
        birth_date=row.data_nascimento,
        sex=row.sexo,
        establishment_number=row.num_estabelecimento,
        schedule_id=row.id_horario,
        internship_end_date=row.data_fim_estagio
    )


def create(nif: int, intern: InternDetails):
    employee.create(nif, EmployeeDetails(intern.fname, intern.lname, intern.zip, intern.locality, intern.street, intern.number, intern.birth_date, intern.sex, intern.establishment_number, intern.schedule_id))  # create employee first
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Estagiario (nif, data_fim_estagio) VALUES (?, ?);",
                nif,
                intern.internship_end_date
            )
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not create intern. Data integrity issue.") from e


def update(nif: int, intern: InternDetails):
    employee.update(nif, EmployeeDetails(intern.fname, intern.lname, intern.zip, intern.locality, intern.street, intern.number, intern.birth_date, intern.sex, intern.establishment_number, intern.schedule_id))  # update employee first
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE Estagiario
                SET data_fim_estagio = ?
                WHERE nif = ?;
                """,
                intern.internship_end_date,
                nif
            )
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not update intern {nif}. Data integrity issue.") from e


def delete(nif: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Estagiario WHERE nif = ?;", nif)
            conn.commit()
            employee.delete(nif)  # delete employee after
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not delete intern {nif}. Data integrity issue.") from e