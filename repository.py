import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    # dict_row allows us to access columns by their names
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    done BOOLEAN
                )
            """)
            cursor.execute("SELECT COUNT(*) FROM tasks")
            count = cursor.fetchone()['count']
            
            if count == 0:
                seed_tasks = [
                    ("Complete FastAPI assignment", False),
                    ("Learn Pydantic models", True),
                    ("Build a Todo API", False)
                ]
                cursor.executemany("INSERT INTO tasks (title, done) VALUES (%s, %s)", seed_tasks)
        conn.commit()

def get_all_tasks():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks")
            return cursor.fetchall()

def get_task_by_id(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            return cursor.fetchone()

def create_task(title: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
                (title, False)
            )
            new_id = cursor.fetchone()['id']
        conn.commit()
        return {"id": new_id, "title": title, "done": False}

def update_task(task_id: int, title: str, done: bool):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s",
                (title, done, task_id)
            )
            rowcount = cursor.rowcount
        conn.commit()
        return rowcount

def delete_task(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            rowcount = cursor.rowcount
        conn.commit()
        return rowcount

def get_task_count():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM tasks")
            return cursor.fetchone()['count']
