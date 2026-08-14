# Task API

A complete, dockerized RESTful Task Management API built with **FastAPI** and **PostgreSQL**. This project demonstrates a production-ready CRUD (Create, Read, Update, Delete) API, fully containerized with persistent volumes.

## Getting Started

You only need one command to run the entire stack (API + Database):

```bash
docker compose up -d
```

### Environment Variables

Before running, make sure you configure your local environment by copying `.env.example` to `.env`. 

```bash
cp .env.example .env
```
*(Note: Never commit your real `.env` file! A leaked database password is a real security incident)*

Your `.env` file should look like this:
```env
DATABASE_URL=postgres://postgres:placeholder@localhost:5433/taskdb
```

---

## API Endpoints

The API is accessible at `http://localhost:3000`.

| Method | Endpoint | Description | Success Status |
|---------|----------|-------------|----------------|
| GET | `/` | API information | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/tasks` | Get all tasks | 200 |
| GET | `/tasks/{id}` | Get a task by ID | 200 / 404 |
| POST | `/tasks` | Create a task | 201 / 400 |
| PUT | `/tasks/{id}` | Update a task | 200 / 404 |
| DELETE | `/tasks/{id}` | Delete a task | 204 / 404 |

---

## Example Usage

### Create a Task

```bash
curl -i -X POST http://localhost:3000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Buy milk"}'
```

**Output:**
```http
HTTP/1.1 201 Created
content-length: 44
content-type: application/json

{
  "id": 1,
  "title": "Buy milk",
  "done": false
}
```

---

## Database Verification

The database volume persists your tasks across container restarts. You can view the data manually using any PostgreSQL GUI (like DBeaver, pgAdmin, or TablePlus).

![Database Screenshot](images/db_screenshot.png)

*(Add your own screenshot of the database table here!)*

*To check manually via `psql` (inside the container):*
```sql
SELECT * FROM tasks;
```

---

## Technologies Used
- **Python** (FastAPI, Uvicorn)
- **PostgreSQL** (with psycopg binary)
- **Docker** & **Docker Compose**