import os
from dotenv import load_dotnev
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

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
