from fastapi import FastAPI,HTTPException

app = FastAPI()

tasks = [
    {
        "id": 1,
        "title": "Complete FastAPI assignment",
        "done": False
    },
    {
        "id": 2,
        "title": "Learn Pydantic models",
        "done": True
    },
    {
        "id": 3,
        "title": "Build a Todo API",
        "done": False
    }
]

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{id}")
async def get_task(id: int):
    try:
        return tasks[id-1]
    except IndexError:
        raise HTTPException(status_code=404, detail="Task not found")



@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return {"status": "ok"}



