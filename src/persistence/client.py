from typing import NamedTuple   
from pyodbc import IntegrityError
from persistence import person
from persistence.person import PersonDetails
from persistence.session import create_connection


class ClientSummary(NamedTuple):
    nif: int
    fname: str
    lname: str


class ClientDetails(PersonDetails):
    phone_number: int


def list_clients() -> list[ClientSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nif, Pnome, Unome FROM Pessoa JOIN Cliente ON Pessoa.nif = Cliente.nif;")
        rows = cursor.fetchall()
        cursor.close()

    clients = []

    for row in rows:
        clients.append(ClientSummary(row.nif, row.Pnome, row.Unome))

    return clients


def list_clients_by_name(name: str) -> list[ClientSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT nif, Pnome, Unome FROM Pessoa JOIN Cliente ON Pessoa.nif = Cliente.nif WHERE Pnome + ' ' + Unome LIKE '%{name}%';")
        rows = cursor.fetchall()
        cursor.close()

    clients = []

    for row in rows:
        clients.append(ClientSummary(row.nif, row.Pnome, row.Unome))

    return clients


def read(nif: int) -> ClientDetails:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pessoa JOIN Cliente ON Pessoa.nif = Cliente.nif WHERE Cliente.nif = ?;", nif)
        row = cursor.fetchone()

    return row.nif, row.num_conta, ClientDetails(
        row.Pnome,
        row.Unome,
        row.cod_postal or "",
        row.localidade or "",
        row.rua or "",
        row.numero or "",
        row.data_nascimento,
        row.sexo,
        row.num_telemovel
    )


def create(nif: int, client: ClientDetails):
    person.create(nif, person.PersonDetails(client.fname, client.lname, client.zip, client.locality, client.street, client.number, client.birth_date, client.sex))  # Create person first
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT MAX(num_conta) FROM Cliente")
            last_cli_row = cursor.fetchone()
            last_cli_acc_num = last_cli_row[0]
            new_cli_acc_num = last_cli_acc_num + 1
            cursor.execute(
                "INSERT INTO Cliente (nif, num_conta, num_telemovel) VALUES (?, ?, ?);",
                nif,
                new_cli_acc_num,
                client.phone_number
            )
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not create client. Data integrity issue.") from e


def update(nif: int, client: ClientDetails):
    person.update(nif, person.PersonDetails(client.fname, client.lname, client.zip, client.locality, client.street, client.number, client.birth_date, client.sex))  # Update person first
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE Cliente 
                SET num_telemovel = ?
                WHERE nif = ?;
                """,
                client.phone_number,
                nif
            )
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not update client {nif}. Data integrity issue.") from e


def delete(nif: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Cliente WHERE nif = ?;", nif)
            conn.commit()
            person.delete(nif)  # Delete person after
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not delete client {nif}. Data integrity issue.") from e
