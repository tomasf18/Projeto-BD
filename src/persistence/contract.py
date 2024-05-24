from dataclasses import dataclass
from typing import NamedTuple
from pyodbc import IntegrityError
from persistence import person
from persistence.person import PersonDetails
from persistence.session import create_connection


class ContractDetails(NamedTuple):
    nif_effective: int
    salary: float
    description: str
    start_date: str
    end_date: str


def read(nif_effective: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Contrato WHERE nif_efetivo = ?", nif_effective)
        row = cursor.fetchone()
        cursor.close()

    return ContractDetails(
        nif_effective=row.nif_efetivo,
        salary=row.salario,
        description=row.descricao,
        start_date=row.data_inicio,
        end_date=row.data_fim
    )


def create_contract(contract: ContractDetails):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Contrato (nif_efetivo, salario, descricao, data_inicio, data_fim) 
                VALUES (?, ?, ?, ?, ?)
                """,
                contract.nif_effective,
                contract.salary,
                contract.description,
                contract.start_date,
                contract.end_date
            )
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not create contract. Data integrity issue.") from e


def update(contract: ContractDetails):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE Contrato
                SET salario = ?, descricao = ?, data_inicio = ?, data_fim = ?
                WHERE nif_efetivo = ?
                """,
                contract.salary,
                contract.description,
                contract.start_date,
                contract.end_date,
                contract.nif_effective
            )
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not update contract {nif_effective}. Data integrity issue.") from e

""" Não quero dar delete ao contrato, quero dar delete ao effective quando é despedido, e o contrato é eliminado em cascata, as edições representam renovações de contrato
def delete_contract(nif_effective: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Contrato WHERE nif_effective = ?", nif_effective)
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not delete contract {nif_effective}. Data integrity issue.") from e
"""