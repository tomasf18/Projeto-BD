from datetime import datetime
from typing import NamedTuple   
from pyodbc import IntegrityError
from persistence.session import create_connection

class Review(NamedTuple):
    emp_nif: int
    cli_nif: int
    review_date: str
    rating: int
    comment: str
    client_Fname: str
    client_Lname: str

def list_reviews_by_num_emp(func_num: int) -> list[Review]:
    with create_connection() as conn:
        cursor = conn.cursor()
        nif = cursor.execute(f"SELECT nif FROM Funcionario WHERE num_funcionario = {func_num};").fetchone()[0]
        cursor.execute(f"SELECT Avaliacao.*, Pessoa.Pnome, Pessoa.Unome FROM Avaliacao JOIN Pessoa ON Avaliacao.nif_cliente = Pessoa.nif WHERE nif_funcionario = {nif};")
        rows = cursor.fetchall()
        cursor.close()

    reviews = []

    for row in rows:
        reviews.append(Review(row.nif_funcionario, row.nif_cliente, row.data_avaliacao.strftime('%Y-%m-%d'), row.n_estrelas, row.comentario, row.Pnome, row.Unome))

    return reviews

def read(nif_emp: int, nif_cli: int, date: str) -> Review:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT Avaliacao.*, Pessoa.Pnome, Pessoa.Unome FROM Avaliacao JOIN Pessoa ON Avaliacao.nif_cliente = Pessoa.nif WHERE nif_funcionario = {nif_emp} AND nif_cliente = {nif_cli} AND CONVERT(date, data_avaliacao) = '{date}';")
        row = cursor.fetchone()
        cursor.close()

    return Review(row.nif_funcionario, row.nif_cliente, row.data_avaliacao, row.n_estrelas, row.comentario, row.Pnome, row.Unome)

def average_rating_by_num_emp(func_num: int) -> float:
    with create_connection() as conn:
        cursor = conn.cursor()
        nif = cursor.execute(f"SELECT nif FROM Funcionario WHERE num_funcionario = {func_num};").fetchone()[0]
        cursor.execute(f"SELECT AVG(CAST(n_estrelas AS FLOAT)) FROM Avaliacao WHERE nif_funcionario = {nif};")
        avg = cursor.fetchone()[0]
        cursor.close()

    return avg

def performance_by_num_emp(func_num: int) -> str:
    with create_connection() as conn:
        cursor = conn.cursor()
        nif = cursor.execute(f"SELECT nif FROM Funcionario WHERE num_funcionario = {func_num};").fetchone()[0]
        cursor.execute("SELECT dbo.get_employee_performance(?)", nif)
        performance = cursor.fetchone()[0]
        cursor.close()

    return performance

def create(emp_nif: int, cli_acc: int, rating: int, comment: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cli_nif = cursor.execute(f"SELECT nif FROM Cliente WHERE num_conta = {cli_acc};").fetchone()[0]
            review_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO Avaliacao VALUES (?, ?, ?, ?, ?)", emp_nif, cli_nif, review_date, rating, comment)
            cursor.commit()
        except IntegrityError:
            raise ValueError("ERROR: could not create review. Data integrity issue.")
        cursor.close()