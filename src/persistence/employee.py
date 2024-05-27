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
    private_phone: str
    company_phone: str


def list_employees() -> list[EmployeeSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                        (SELECT num_funcionario, Pnome, Unome 
                        FROM Pessoa 
                        JOIN Funcionario ON Pessoa.nif = Funcionario.nif 
                        JOIN Efetivo ON Funcionario.nif = Efetivo.nif) 
                        UNION 
                        (SELECT num_funcionario, Pnome, Unome 
                        FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif 
                        JOIN Estagiario ON Funcionario.nif = Estagiario.nif)
                        ORDER BY num_funcionario
                       """)
        rows = cursor.fetchall()
        cursor.close()

    employees = []

    for row in rows:
        employees.append(EmployeeSummary(row.num_funcionario, row.Pnome, row.Unome))

    return employees

def list_employees_by_establishment(establishment_number: int) -> list[EmployeeSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
                        SELECT num_funcionario, Pnome, Unome
                        FROM Funcionario
                        JOIN Pessoa ON Funcionario.nif = Pessoa.nif
                        WHERE Funcionario.num_estabelecimento = {establishment_number} 
                       """)
        rows = cursor.fetchall()
        cursor.close()

    employees = []

    for row in rows:
        employees.append(EmployeeSummary(row.num_funcionario, row.Pnome, row.Unome))

    return employees


def list_employees_by_name(name: str) -> list[EmployeeSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
                        SELECT * 
						FROM  ((SELECT num_funcionario, Pnome, Unome 
								FROM Pessoa 
								JOIN Funcionario ON Pessoa.nif = Funcionario.nif 
								JOIN Efetivo ON Funcionario.nif = Efetivo.nif) 
								UNION 
							   (SELECT num_funcionario, Pnome, Unome 
								FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif 
								JOIN Estagiario ON Funcionario.nif = Estagiario.nif)) AS Employees
						WHERE Pnome + ' ' + Unome LIKE '%{name}%'
                        ORDER BY num_funcionario
                       """)
        rows = cursor.fetchall()
        cursor.close()

    employees = []

    for row in rows:
        employees.append(EmployeeSummary(row.num_funcionario, row.Pnome, row.Unome))

    return employees


def read(emp_num: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM get_employee_details(?)", emp_num)
        row = cursor.fetchone()

    return row.nif, emp_num, EmployeeDetails(
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
        company_phone=row.company_phone
    )


def create(nif: int, employee: EmployeeDetails):
    person.create(nif, PersonDetails(employee.fname, employee.lname, employee.zip, employee.locality, employee.street, employee.number, employee.birth_date, employee.sex))  # create person first
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(num_funcionario) FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif")
        last_emp_row = cursor.fetchone()
        last_emp_num = last_emp_row[0]
        new_emp_num = last_emp_num + 1
        try:
            cursor.execute(
                """
                EXEC CreateEmployee ?, ?, ?, ?, ?, ?
                """,
                nif,
                new_emp_num,
                employee.establishment_number,
                employee.schedule_id,
                employee.private_phone,
                employee.company_phone
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
                EXEC UpdateEmployeeDetails ?, ?, ?, ?, ?
                """,
                employee.establishment_number,
                employee.schedule_id,
                nif,
                employee.company_phone,
                employee.private_phone,
            )
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not update employee {nif}. Data integrity issue.") from e


def delete(nif: int):
    try:
        person.delete(nif)  # delete the correspondent person, because it will activate the trigger to delete the employee and effective/intern
    except IntegrityError as e:
        if e.args[0] == '23000':
            raise ValueError(f"ERROR: could not delete employee {nif}. Data integrity issue.") from e