from dataclasses import dataclass
from typing import List, NamedTuple
from pyodbc import IntegrityError
from persistence import employee
from persistence.employee import EmployeeDetails
from persistence.session import create_connection
from persistence.contract import ContractDetails
from persistence import contract, person


class EffectiveSummary(NamedTuple):
    employee_number: int
    fname: str
    lname: str
    type: str = "E"

@dataclass
class EffectiveDetails(EmployeeDetails):
    specialities: List[str]
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
        rows = cursor.fetchall()
        specialities_list = []
        for row in rows:
            if row.speciality:
                specialities_list.append(row.speciality)

        contract_details = contract.read(rows[0].nif)

    return rows[0].nif, emp_num, EffectiveDetails(
        fname=rows[0].fname,
        lname=rows[0].lname,
        zip=rows[0].zip or "",
        locality=rows[0].locality or "",
        street=rows[0].street or "",
        number=rows[0].number or "",
        birth_date=rows[0].birth_date,
        sex=rows[0].sex,
        establishment_number=rows[0].establishment_number,
        schedule_id=rows[0].schedule_id,
        private_phone=rows[0].private_phone,
        company_phone=rows[0].company_phone,
        specialities=specialities_list,
        manager=rows[0].manager, 
        contract=contract_details
    )


def create(nif: int, effective: EffectiveDetails):
    employee.create(nif, EmployeeDetails(effective.fname, effective.lname, effective.zip, effective.locality, effective.street, effective.number, effective.birth_date, effective.sex, effective.establishment_number, effective.schedule_id, effective.private_phone, effective.company_phone))  # create employee first
    contract_details = effective.contract
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Efetivo (nif) VALUES (?);
                INSERT INTO Contrato (nif_efetivo, salario, descricao, data_inicio, data_fim) VALUES (?, ?, ?, ?, ?);
                """,
                nif,
                nif,
                contract_details.salary,
                contract_details.description,
                contract_details.start_date,
                contract_details.end_date
            )
            for speciality in effective.specialities:
                cursor.execute("EXEC CreateTem ?, ?;", nif, speciality)
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not create effective. Data integrity issue.") from e


def update(nif: int, effective: EffectiveDetails):
    employee.update(nif, EmployeeDetails(fname=effective.fname, lname=effective.lname, zip=effective.zip, locality=effective.locality, street=effective.street, number=effective.number, birth_date=effective.birth_date, sex=effective.sex,establishment_number=effective.establishment_number, schedule_id=effective.schedule_id, private_phone=effective.private_phone, company_phone=effective.company_phone)) # update employee first
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                DELETE FROM Tem WHERE nif_efetivo = ?;
                INSERT INTO Contrato (nif_efetivo, salario, descricao, data_inicio, data_fim) VALUES (?, ?, ?, ?, ?);
                """,
                nif,
                nif,
                effective.contract.salary,
                effective.contract.description,
                effective.contract.start_date,
                effective.contract.end_date
            )
            for speciality in effective.specialities:
                cursor.execute("EXEC CreateTem ?, ?;", nif, speciality)
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not update effective {nif}. Data integrity issue.") from e


def delete(nif: int):
    try:
        person.delete(nif)  # delete the correspondent person, because it will activate the trigger to delete the employee and effective/intern
    except IntegrityError as e:
        if e.args[0] == '23000':
            raise ValueError(f"ERROR: could not delete effective {nif}. Data integrity issue.") from e
            

def isEffective(emp_num: int) -> bool:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT num_funcionario FROM Efetivo JOIN Funcionario ON Efetivo.nif=Funcionario.nif WHERE num_funcionario = ?", emp_num)
        row = cursor.fetchone()
        return row is not None
