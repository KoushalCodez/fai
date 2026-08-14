from fastapi.testclient import TestClient
from server import app

def run_crud_tests():
    with TestClient(app) as client:
        # 1. Create a task (POST /tasks)
        response = client.post("/tasks", json={"title": "Test CRUD Task"})
        print(f"POST /tasks -> {response.status_code}")
        assert response.status_code == 201
        
        task_id = response.json()["id"]
        print(f"Created task with id: {task_id}")

        # 2. Mark it done (PUT /tasks/{id})
        response = client.put(f"/tasks/{task_id}", json={"title": "Test CRUD Task", "done": True})
        print(f"PUT /tasks/{task_id} -> {response.status_code}")
        assert response.status_code == 200

        # 3. Confirm with GET /tasks/{id}
        response = client.get(f"/tasks/{task_id}")
        print(f"GET /tasks/{task_id} -> {response.status_code}")
        assert response.status_code == 200
        assert response.json()["done"] is True

        # 4. DELETE it (DELETE /tasks/{id})
        response = client.delete(f"/tasks/{task_id}")
        print(f"DELETE /tasks/{task_id} -> {response.status_code}")
        assert response.status_code == 204

        # 5. GET /tasks/{id} to confirm it's gone
        response = client.get(f"/tasks/{task_id}")
        print(f"GET /tasks/{task_id} -> {response.status_code}")
        assert response.status_code == 404

        print("\nAll checks passed successfully!")

if __name__ == "__main__":
    run_crud_tests()
