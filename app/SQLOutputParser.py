from langchain.schema import BaseOutputParser
from typing import Dict, Any
import re

class SQLOutputParser(BaseOutputParser):
  def parse(self, text: str) -> Dict[str, Any]:
    sql_match = re.search(r'```sql\n(.*?)\n```', text, re.DOTALL)

    if sql_match:
      sql_query = sql_match.group(1).strip()
    else:
      sql_match = re.search(r'(SELECT.*?;?)', text, re.IGNORECASE | re.DOTALL)
      sql_query = sql_match.group(1).strip() if sql_match else text.strip()

    return {
      "sql_query": sql_query,
      "raw_response": text,
      "confidence": "high" if "SELECT" in sql_query.upper() else "low"
    }
