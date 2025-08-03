from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="SQL Dashboard API", version="1.0.0")

class QueryRequest(BaseModel):
  question: str
  database_name: Optional[str] = "default"

class QueryResponse(BaseModel):
  sql_query: str
  execution_time: float
  row_count: int

@app.get("/")
async def root():
  return { "message": "SQL Dashboard API" }

@app.get("/health")
async def health_check():
  return { "status": "healthy" }

async def generate_sql(request: QueryRequest):
  return QueryResponse(
    sql_query="SELECT * FROM users WHERE name ILIKE '%{request.question}%'",
    execution_time=0.123,
    row_count=42
  )

