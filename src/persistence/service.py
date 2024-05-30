from typing import NamedTuple   
from pyodbc import IntegrityError # type: ignore
from persistence.session import create_connection

class ServiceType(NamedTuple):
    sex: str
    designation: str

class ServiceDetails(NamedTuple):
    sex: str
    designation: str
    name: str
    price: float


def list_services() -> list[ServiceType]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tipo_servico;")
        rows = cursor.fetchall()
        cursor.close()

    services = []

    for row in rows:
        services.append(ServiceType(row.sexo, row.designacao))

    return services

def list_services_by_type(serv_type: str) -> list[ServiceType]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Tipo_servico WHERE designacao LIKE '%{serv_type}%';")
        rows = cursor.fetchall()
        cursor.close()

    services = []

    for row in rows:
        services.append(ServiceType(row.sexo, row.designacao))
    
    return services

def read(sex: str, designation: str) -> list[ServiceDetails]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM Servico WHERE sexo = ? AND designacao = ?;""", (sex, designation))
        rows = cursor.fetchall()
        cursor.close()
    
    services = []

    for row in rows:
        services.append(ServiceDetails(row.sexo, row.designacao, row.nome, row.preco) )
    return services

def delete(sex: str, designation: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM Tipo_servico WHERE sexo = ? AND designacao = ?;""", (sex, designation))
            conn.commit()
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError("Cannot delete this service type.")

def create(service: ServiceDetails):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Tipo_servico (sexo, designacao) VALUES (?, ?);
                """, service.sex, service.designation)
            
            cursor.execute(
                """
                INSERT INTO Servico (nome, preco, sexo, designacao) VALUES (?, ?, ?, ?);
                """, service.name, service.price, service.sex, service.designation)
            conn.commit()
            return service.designation
        except IntegrityError as e:
            if e.args[0] == '23000':
                raise ValueError("Cannot create this service type.")
