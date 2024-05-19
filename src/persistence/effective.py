from dataclasses import dataclass
from typing import NamedTuple
from pyodbc import IntegrityError
from persistence import employee
from persistence.employee import EmployeeDetails
from persistence.session import create_connection


class EffectiveSummary(NamedTuple):
    employee_number: int
    fname: str
    lname: str
    type: str = "E"


@dataclass
class EffectiveDetails(EmployeeDetails):
    pass  # no additional fields needed, inherits everything from EmployeeDetails


def list_effectives() -> list[EffectiveSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT num_funcionario, Pnome, Unome FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif JOIN Efetivo ON Funcionario.nif = Efetivo.nif")
        rows = cursor.fetchall()
        cursor.close()

    effectives = []

    for row in rows:
        effectives.append(EffectiveSummary(row.num_funcionario, row.Pnome, row.Unome))

    return effectives


def list_effectives_by_name(name: str) -> list[EffectiveSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT num_funcionario, Pnome, Unome FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif JOIN Efetivo ON Funcionario.nif = Efetivo.nif WHERE Pnome + ' ' + Unome LIKE '%{name}%';")
        rows = cursor.fetchall()
        cursor.close()

    effectives = []

    for row in rows:
        effectives.append(EffectiveSummary(row.num_funcionario, row.Pnome, row.Unome))

    return effectives


def read(emp_num: int) -> EffectiveDetails:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pessoa JOIN Funcionario ON Pessoa.nif = Funcionario.nif JOIN Efetivo ON Funcionario.nif = Efetivo.nif WHERE num_funcionario = ?;", emp_num)
        row = cursor.fetchone()

    return row.nif, row.num_funcionario, EffectiveDetails(
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


def create(nif: int, effective: EffectiveDetails):
    employee.create(nif, EmployeeDetails(effective.fname, effective.lname, effective.zip, effective.locality, effective.street, effective.number, effective.birth_date, effective.sex, effective.establishment_number, effective.schedule_id))  # create employee first
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Efetivo (nif) VALUES (?);",
                nif
            )
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not create effective. Data integrity issue.") from e


def update(nif: int, effective: EffectiveDetails):
    employee.update(nif, EmployeeDetails(fname=effective.fname, 
                                         lname=effective.lname, 
                                         zip=effective.zip, 
                                         locality=effective.locality, 
                                         street=effective.street, 
                                         number=effective.number, 
                                         birth_date=effective.birth_date, 
                                         sex=effective.sex,
                                         establishment_number=effective.establishment_number, 
                                         schedule_id=effective.schedule_id)) # update employee first
    # no specific update needed for Efetivo, because it has no additional fields


def delete(nif: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Efetivo WHERE nif = ?;", nif)
            conn.commit()
            employee.delete(nif)  # delete employee after
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not delete effective {nif}. Data integrity issue.") from e
            

def isEffective(emp_num: int) -> bool:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT num_funcionario FROM Efetivo JOIN Funcionario ON Efetivo.nif=Funcionario.nif WHERE num_funcionario = ?", emp_num)
        row = cursor.fetchone()
        return row is not None
