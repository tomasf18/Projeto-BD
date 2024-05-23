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
    speciality: str
    manager: bool
    contract: ContractDetails


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
        cursor.execute("SELECT * FROM dbo.get_effective_details(?);", emp_num)
        row = cursor.fetchone()

    return row.nif, row.num_funcionario, EffectiveDetails (
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
        speciality=row.speciality,
        manager=row.manager
    )


def create(nif: int, effective: EffectiveDetails):
    employee.create(nif, EmployeeDetails(effective.fname, effective.lname, effective.zip, effective.locality, effective.street, effective.number, effective.birth_date, effective.sex, effective.establishment_number, effective.schedule_id, effective.private_phone, effective.company_phone))  # create employee first
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Efetivo (nif) VALUES (?);
                INSERT INTO Tem (nif_efetivo, especialidade) VALUES (?, ?);
                inserir contrato
                """,
                nif,
                nif,
                effective.speciality
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
