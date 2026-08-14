from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.responses import JSONResponse
import repository

@asynccontextmanager
async def lifespan(app: FastAPI):
    # First-run: Setup DB on startup
    repository.init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/tasks", summary="get all tasks")
async def get_tasks():
    return repository.get_all_tasks()

@app.get("/tasks/{id}", summary="Get a task by ID")
async def get_task(id: int):
    task = repository.get_task_by_id(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="create a new task")
async def create_task(t: dict):
    title = t.get("title")
    if not title or str(title).strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")
        
    return repository.create_task(title)

@app.put("/tasks/{id}", summary="update a task")
async def update_task(id: int, t: dict):
    title = t.get("title")
    done = t.get("done")

    if title is None or str(title).strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")

    rowcount = repository.update_task(id, title, bool(done))
    
    if rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"id": id, "title": title, "done": bool(done)}

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="delete a task")
async def delete_task(id: int):
    rowcount = repository.delete_task(id)
    
    if rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/", summary="get the task api docs")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health", summary="get the health of the task api")
async def health():
    count = repository.get_task_count()
    return {"status": "ok", "length": count}
