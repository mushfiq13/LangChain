from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"message": "SQL Dashboard API"}

def test_generate_sql():
  response = client.post(
    "/generate-sql",
    json={"question": "Show all users", "database_name": "test"}
  )
  assert response.status_code == 200
  data = response.json()
  assert "sql_query" in data
