from fastapi import FastAPI, HTTPException, status

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

@app.get("/tasks", summary="get all tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{id}", summary="Get a task by ID")
async def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="create a new task")
async def create_task(t:dict):
    title= t.get("title")
    if not title or title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")
    new_task_id = len(tasks) + 1
    new_task = {
        "id": new_task_id,
        "title": title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{id}", summary="update a task")
async def update_task(id: int, t: dict):
    for task in tasks:
        if task["id"] == id:
            title = t.get("title")
            done = t.get("done")

            if title is None or title.strip() == "":
                raise HTTPException(
                    status_code=400,
                    detail="Title is required"
                )

            task["title"] = title
            task["done"] = done

            return task

    raise HTTPException(status_code=404, detail="Task not found")

from fastapi import Response

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="delete a task")
async def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/",summary="get the task api docs")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health",summary="get the health of the task api")
async def health():
    return {"status": "ok", "length": len(tasks)}
