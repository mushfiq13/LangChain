import os
import SQLOutputParser

from dotenv import load_dotnev
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain.chains import SQLDatabaseChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotnev()

# Initialize LLM
llm = OpenAI(temperature=0.7, open_api_key=os.getenv("OPENAI_API_KEY"))

# Create prompt template
sql_prompt = PromptTemplate(
  input_variables=["question", "schema"],
  template="""
  Given the database schema:
  {schema}

  Generate a SQL query for: {question}

  SQL Query:
  """
)

# Create chain
sql_chain = LLMChain(llm=llm, prompt=sql_prompt)

# Test the chain
schema = "Tables: users(id, name, email), orders(id, user_id, amount, date)"
result = sql_chain.run(question="Find users who spent more than $100", schema=schema)
print(result)

# Enhanced SQL chain with parser
enhanced_prompt = PromptTemplate(
  input_variables=["question", "schema"],
  template="""
  Database Schema: {schema}
  Question: {question}

  Generate a SQL query. Format your response as
  ```sql
  YOUR_SQL_QUERY_HERE
  ```
  """
)

sql_chain_with_parser = LLMChain(
  llm=llm,
  prompt=enhanced_prompt,
  output_parser=SQLOutputParser()
)

# Create in-memory SQLite database for testing
engine = create_engine("sqlite:///test.db")
db = SQLDatabase.from_uri("sqlite:///test.db")

# Create SQL Database Chain
sql_db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

memory = ConversationBufferMemory()
conversation = ConversationChain(
  llm=llm,
  memory=memory,
  verbose=True
)
