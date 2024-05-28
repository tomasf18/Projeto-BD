from typing import NamedTuple   
from pyodbc import IntegrityError # type: ignore
from persistence.session import create_connection

class ServiceType(NamedTuple):
    sex: str
    designation: str

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