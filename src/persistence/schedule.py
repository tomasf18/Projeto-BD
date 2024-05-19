from typing import NamedTuple   
from pyodbc import IntegrityError
from persistence.session import create_connection


class ScheduleDetails(NamedTuple):
    id: str
    day_off: str
    start_time: str
    end_time: str


def list_schedules() -> list[ScheduleDetails]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Horario;")
        rows = cursor.fetchall()
        cursor.close()

    schedules = []

    for row in rows:
        schedules.append(ScheduleDetails(row.id, row.dia_folga, row.h_entrada, row.h_saida))

    return schedules


def list_schedules_by_day_off(day: str) -> list[ScheduleDetails]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Horario WHERE dia_folga LIKE '%{day}%';")
        rows = cursor.fetchall()
        cursor.close()

    schedules = []

    for row in rows:
        schedules.append(ScheduleDetails(row.id, row.dia_folga, row.h_entrada, row.h_saida))

    return schedules


def read(schedule_id: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Horario WHERE id = ?;", schedule_id)
        row = cursor.fetchone()

    return ScheduleDetails(
        row.id,
        row.dia_folga,
        row.h_entrada,
        row.h_saida
    )


def create(schedule: ScheduleDetails):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM Horario")
        last_schedule_row = cursor.fetchone()
        last_schedule_id = last_schedule_row[0]
        new_schedule_id = last_schedule_id + 1
        try:
            cursor.execute("INSERT INTO Horario VALUES (?, ?, ?, ?);", new_schedule_id, schedule.day_off, schedule.start_time, schedule.end_time)
            conn.commit()
        except IntegrityError as e:
            raise ValueError(f"ERROR: could not create schedule. Data integrity issue.") from e
        

def update(schedule: ScheduleDetails):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Horario SET dia_folga = ?, h_entrada = ?, h_saida = ? WHERE id = ?;", schedule.day_off, schedule.start_time, schedule.end_time, schedule.id)
            conn.commit()
        except IntegrityError as e:
            raise ValueError(f"ERROR: could not update schedule {schedule.id}. Data integrity issue.") from e
        

def delete(id: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Horario WHERE id = ?;", id)
            conn.commit()
        except IntegrityError as e:
            raise ValueError(f"ERROR: could not delete schedule {id}. Data integrity issue.") from e
        

def get_schedule_of_emp(emp_num: int):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT num_funcionario, id, dia_folga, h_entrada, h_saida FROM Funcionario JOIN Horario ON id_horario=id WHERE num_funcionario = ?;", emp_num)
        row = cursor.fetchone()

    return ScheduleDetails(row.id, row.dia_folga, row.h_entrada, row.h_saida)