from fastapi import FastAPI, HTTPException, status
import sqlite3

app = FastAPI()

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        done BOOLEAN
    )
""")

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    seed_tasks = [
        ("Complete FastAPI assignment", 0),
        ("Learn Pydantic models", 1),
        ("Build a Todo API", 0)
    ]
    cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", seed_tasks)
    conn.commit()
conn.close()



@app.get("/tasks", summary="get all tasks")
async def get_tasks():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    db_tasks = [{"id": row["id"], "title": row["title"], "done": bool(row["done"])} for row in cursor.fetchall()]
    conn.close()
    return db_tasks

@app.get("/tasks/{id}", summary="Get a task by ID")
async def get_task(id: int):
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
        
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="create a new task")
async def create_task(t:dict):
    title = t.get("title")
    if not title or title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")
        
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, False))
    conn.commit()
    new_task_id = cursor.lastrowid
    conn.close()
    
    return {
        "id": new_task_id,
        "title": title,
        "done": False
    }

@app.put("/tasks/{id}", summary="update a task")
async def update_task(id: int, t: dict):
    title = t.get("title")
    done = t.get("done")

    if title is None or title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (title, done, id))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
        
    conn.commit()
    conn.close()

    return {"id": id, "title": title, "done": bool(done)}

from fastapi import Response

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="delete a task")
async def delete_task(id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
        
    conn.commit()
    conn.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/",summary="get the task api docs")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health",summary="get the health of the task api")
async def health():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    conn.close()
    return {"status": "ok", "length": count}
