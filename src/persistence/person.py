from dataclasses import dataclass
import random
import string
from typing import NamedTuple   
from pyodbc import IntegrityError
from persistence.session import create_connection


class PersonSummary(NamedTuple):
    nif: str
    fname: str
    lname: str

@dataclass
class PersonDetails:
    fname: str
    lname: str
    zip: str
    locality: str
    street: str
    number: str
    birth_date: str
    sex: str
    

def list_persons() -> list[PersonSummary]:
    
    with create_connection() as conn:  
        cursor = conn.cursor()     
        cursor.execute("SELECT nif, Pnome, Unome FROM Pessoa") 
        rows = cursor.fetchall()
        cursor.close()

    persons = []

    for row in rows:
        persons.append(PersonSummary(row.nif, row.Pnome, row.Unome)) 

    return persons


def list_persons_by_name(name: str) -> list[PersonSummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT nif, Pnome, Unome FROM Pessoa WHERE Pnome + ' ' + Unome LIKE '%{name}%';")
        rows = cursor.fetchall()
        cursor.close()

    persons = []

    for row in rows:
        persons.append(PersonSummary(row.nif, row.Pnome, row.Unome))

    return persons


def read(nif: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pessoa WHERE nif = ?;", nif)
        row = cursor.fetchone()

        return row.nif, PersonDetails(
            row.Pnome,
            row.Unome,
            row.cod_postal or "",
            row.localidade or "",
            row.rua or "",
            row.numero or "",
            row.data_nascimento,
            row.sexo
        )
    

def create(nif: int, person: PersonDetails):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Pessoa (Pnome, Unome, nif, cod_postal, localidade, rua, numero, data_nascimento, sexo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
                person.fname,
                person.lname,
                nif,
                person.zip,
                person.locality,
                person.street,
                person.number,
                person.birth_date,
                person.sex
            )
            
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not create person. Data integrity issue.") from e
        

def update(nif: int, person: PersonDetails):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE Pessoa 
                SET Pnome = ?, Unome = ?, cod_postal = ?, localidade = ?, rua = ?, numero = ?, data_nascimento = ?, sexo = ? 
                WHERE nif = ?;
                """,
                person.fname,
                person.lname,
                person.zip,
                person.locality,
                person.street,
                person.number,
                person.birth_date,
                person.sex,
                nif
            )
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not update person {nif}. Data integrity issue.") from e


def delete(nif: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Pessoa WHERE nif = ?;", nif)
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError(f"ERROR: could not delete person {nif}. Data integrity issue.") from e
