from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from time import time
from http.client import HTTPException
import json
from fastapi import BackgroundTasks

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

@app.post("/generate-sql", response_model=QueryResponse)
async def generate_sql(request: QueryRequest):
  return QueryResponse(
    sql_query="SELECT * FROM users WHERE name ILIKE '%{request.question}%'",
    execution_time=0.123,
    row_count=42
  )

@app.post("/execute-sql")
async def execute_sql(
    request: QueryRequest,
    db = Depends(get_database_connection)
):
  return {"query": request.question, "db_status": db["connection"]}

@app.post("/upload-schema")
async def upload_database_schema(file: UploadFile = File(...)):
  if not file.filename.endswith(".json"):
    raise HTTPException(status_code=400, detail="Only JSON files allowed")

  content = await file.read()
  schema_data = json.loads(content)
  return {"filename": file.filename, "tables": len(schema_data.get("tables", []))}

@app.get("/download-results/{query_id}")
async def download_results(query_id: str):
  return FileResponse(
    path=f"results_{query_id}.csv",
    filename=f"query_resutls_{query_id}.csv",
    media_type="text/csv"
  )

def process_large_query(query: str):
  time.sleep(5)  # Simulate long processing time
  print(f"Processed query: {query}")

async def create_async_query(
    request: QueryRequest,
    background_tasks: BackgroundTasks
):
  background_tasks.add_tasks(process_large_query, request.question)
  return {"message": "Query submitted for processing"}
