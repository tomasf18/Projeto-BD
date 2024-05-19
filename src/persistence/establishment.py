import random
import string
from typing import NamedTuple   # module that allows to define/create named data types (named tuples) that are immutable
from pyodbc import IntegrityError
from persistence.session import create_connection


class EstablishmentSummary(NamedTuple): # named tuple that represents a establishment
    id: int
    specification: str


class EstablishmentDetails(NamedTuple): # named tuple that represents a establishment
    # this is a subclass of NamedTuple and serves as a basic descriptor for establishments
    specification: str
    zip: str
    locality: str
    street: str
    number: int
    manager_nif: int
    manager_init_date: str


def list_establishments() -> list[EstablishmentSummary]:
    # create a connection to the database (using 'with' statement to ensure that the connection is closed after the block is executed)
    with create_connection() as conn: 
        # create a cursor object to execute SQL queries and iterate over the results 
        cursor = conn.cursor()     
        # execute a query to select all establishments
        cursor.execute("SELECT id, especificacao FROM Estabelecimento") 
        # fetch all rows from the result of the query (returns a list of tuples like: [(...), (1, 'Restaurante', '4000-007', 'Porto', 'Rua do Almada', 13, 123456789, '2020-01-01'), (...)]
        rows = cursor.fetchall()
        # close the cursor
        cursor.close()

    establishments = []

    # iterate over the rows and create a named tuple for each row
    for row in rows:
        establishments.append(EstablishmentSummary(row.id, row.especificacao)) 

    # return a list of establishments, where each establishment is a named tuple
    return establishments


def list_establishments_by_locality(local: str) -> list[EstablishmentSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, especificacao FROM Estabelecimento WHERE localidade LIKE '%{local}%';")
        rows = cursor.fetchall()
        cursor.close()

    establishments = []

    for row in rows:
        establishments.append(EstablishmentSummary(row.id, row.especificacao))

    return establishments


def read(est_id: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Estabelecimento WHERE id = ?;", est_id)
        row = cursor.fetchone()

        return row.id, EstablishmentDetails(
            row.especificacao, 
            row.cod_postal or "", 
            row.localidade or "", 
            row.rua or "", 
            row.numero or "", 
            row.nif_gerente, 
            row.data_inicio_gerente
        )
    

def create(establishment: EstablishmentDetails):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT MAX(id) FROM Estabelecimento")
            last_est_row = cursor.fetchone()
            last_est_id = last_est_row[0]
            new_est_id = last_est_id + 1
            cursor.execute(
                "INSERT INTO Estabelecimento (id, especificacao, cod_postal, localidade, rua, numero, nif_gerente, data_inicio_gerente) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                new_est_id,
                establishment.specification,
                establishment.zip,
                establishment.locality,
                establishment.street,
                establishment.number,
                establishment.manager_nif,
                establishment.manager_init_date
            )
            # commit the transaction, saving it in the database (class 10)
            conn.commit()
            return new_est_id
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not create establishment. Data integrity issue.") from e
        

def update(est_id: int, establishment: EstablishmentDetails):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE Estabelecimento 
                SET especificacao = ?, cod_postal = ?, localidade = ?, rua = ?, numero = ?, nif_gerente = ?, data_inicio_gerente = ? 
                WHERE id = ?;
                """,
                establishment.specification,
                establishment.zip,
                establishment.locality,
                establishment.street,
                establishment.number,
                establishment.manager_nif,
                establishment.manager_init_date,
                est_id
            )
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not update establishment {est_id}. Data integrity issue.") from e


def delete(est_id: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Estabelecimento WHERE id = ?;", est_id)
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not delete establishment {est_id}. Data integrity issue.") from e
