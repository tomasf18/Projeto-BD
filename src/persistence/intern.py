from dataclasses import dataclass
from typing import NamedTuple
from pyodbc import IntegrityError
from persistence import employee, person
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
        cursor.execute("SELECT * FROM get_intern_details(?);", emp_num)
        row = cursor.fetchone()

    return row.nif, emp_num, InternDetails(
        fname=row.fname,
        lname=row.lname,
        zip=row.zip or "",
        locality=row.locality or "",
        street=row.street or "",
        number=row.number or "",
        birth_date=row.birth_date,
        sex=row.sex,
        establishment_number=row.establishment_number,
        schedule_id=row.schedule_id,
        private_phone=row.private_phone,
        company_phone=row.company_phone,
        internship_end_date=row.internship_end_date
    )


def create(nif: int, intern: InternDetails):
    employee.create(nif, EmployeeDetails(intern.fname, intern.lname, intern.zip, intern.locality, intern.street, intern.number, intern.birth_date, intern.sex, intern.establishment_number, intern.schedule_id, intern.private_phone, intern.company_phone))  # create employee first
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
    employee.update(nif, EmployeeDetails(fname=intern.fname, lname=intern.lname, zip=intern.zip, locality=intern.locality, street=intern.street, number=intern.number, birth_date=intern.birth_date, sex=intern.sex,establishment_number=intern.establishment_number, schedule_id=intern.schedule_id, private_phone=intern.private_phone, company_phone=intern.company_phone)) # update employee first
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
    try:
        person.delete(nif)  # delete the correspondent person, because it will activate the trigger to delete the employee and effective/intern
    except IntegrityError as e:
        if e.args[0] == '23000':
            raise ValueError(f"ERROR: could not delete intern {nif}. Data integrity issue.") from e
