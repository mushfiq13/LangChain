from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from time import time

class QueryRequest(BaseModel):
  question: str
  database_name: Optional[str] = "default"

class QueryResponse(BaseModel):
  sql_query: str
  execution_time: float
  row_count: int

app = FastAPI(title="SQL Dashboard API", version="1.0.0")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

async def add_process_time_header(request, call_next):
  start_time = time.time()
  response = await call_next(request)
  process_time = time.time() - start_time
  response.headers["X-Process-Time"] = str(process_time)
  return response

async def get_database_connection():
  return {"connection": "active"}

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

@app.post("/execute_sql")
async def execute_sql(
    request: QueryRequest,
    db = Depends(get_database_connection)
):
  return {"query": request.question, "db_status": db["connection"]}
