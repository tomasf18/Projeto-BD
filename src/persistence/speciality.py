from typing import NamedTuple   
from pyodbc import IntegrityError
from persistence.session import create_connection

class SpecialitySummary(NamedTuple):
    designation: str

def list_specialities() -> list[SpecialitySummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Especialidade;")
        rows = cursor.fetchall()
        cursor.close()
    
    specialities = []

    for row in rows:
        specialities.append(SpecialitySummary(row.designacao))
    
    return specialities

def list_specialities_by_designation(designation: str) -> list[SpecialitySummary]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Especialidade WHERE designacao LIKE '%{designation}%';")
        rows = cursor.fetchall()
        cursor.close()
    
    specialities = []

    for row in rows:
        specialities.append(SpecialitySummary(row.designacao))
    
    return specialities

def create(speciality: SpecialitySummary):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Especialidade (designacao) VALUES (?);", speciality.designation)
            conn.commit()
        except IntegrityError as e:
            raise ValueError(f"ERROR: could not create speciality. Data integrity issue.") from e

def delete(speciality_designation: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Especialidade WHERE designacao = ?;", speciality_designation)
            conn.commit()
        except IntegrityError as e:
            raise ValueError(f"ERROR: could not delete speciality {speciality_designation}. Data integrity issue.") from e
