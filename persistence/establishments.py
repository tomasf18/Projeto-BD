import random
import string
from typing import NamedTuple   # module that allows to define/create named data types (named tuples) that are immutable

from pyodbc import IntegrityError

from persistence.session import create_connection

class EstablishmentsDetails(NamedTuple): # named tuple that represents a establishment
    # This is a subclass of NamedTuple and serves as a basic descriptor for establishments
    id: int
    specification: str
    zip: str
    locality: str
    street: str
    number: int
    manager_nif: int
    manager_init_date: str

def list_establishments() -> list[EstablishmentsDetails]:
    # create a connection to the database (using 'with' statement to ensure that the connection is closed after the block is executed)
    with create_connection() as conn: 
        # create a cursor object to execute SQL queries and iterate over the results 
        cursor = conn.cursor()     
        # execute a query to select all establishments
        cursor.execute("SELECT * FROM Estabelecimento") 
        # fetch all rows from the result of the query (returns a list of tuples like: [(...), (1, 'Restaurante', '4000-007', 'Porto', 'Rua do Almada', 13, 123456789, '2020-01-01'), (...)]
        rows = cursor.fetchall()
        # close the cursor
        cursor.close()

    establishments = []

    # iterate over the rows and create a named tuple for each row
    for row in rows:
        establishments.append(EstablishmentsDetails(row.id, row.especificacao, row.cod_postal, row.localidade, row.rua, row.numero, row.nif_gerente, row.data_inicio_gerente)) # or just EstablishmentsDetails(*row)

    # return a list of establishments, where each establishment is a named tuple
    return establishments


def read(est_id: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Estabelecimento WHERE id = ?;", est_id)
        row = cursor.fetchone()

        return EstablishmentsDetails(
            row.id, 
            row.especificacao, 
            row.cod_postal, 
            row.localidade, 
            row.rua, 
            row.numero, 
            row.nif_gerente, 
            row.data_inicio_gerente
        )
    
def create(establishment: EstablishmentsDetails):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Estabelecimento (id, especificacao, cod_postal, localidade, rua, numero, nif_gerente, data_inicio_gerente) VALUES (?, ?, ?, ?, ?, ?, ?);",
                establishment.id,
                establishment.specification,
                establishment.zip,
                establishment.locality,
                establishment.street,
                establishment.number,
                establishment.manager_nif,
                establishment.manager_init_date
            )
            conn.commit()
        except IntegrityError:
            conn.rollback()
            raise ValueError("NIF do gerente não existe na tabela Gerente")
        
def update(establishment: EstablishmentsDetails):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Estabelecimento SET id = ?, especificacao = ?, cod_postal = ?, localidade = ?, rua = ?, numero = ?, nif_gerente = ?, data_inicio_gerente = ? WHERE id = ?;",
            # Gerir questão do id, não pode ser mudado!!! (Fazer como sor)
            establishment.id,
            establishment.specification,
            establishment.zip,
            establishment.locality,
            establishment.street,
            establishment.number,
            establishment.manager_nif,
            establishment.manager_init_date,
            establishment.id
        )
        conn.commit()




