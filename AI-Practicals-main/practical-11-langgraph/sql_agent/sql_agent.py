import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from llm.bedrock import llm

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


# -----------------------------------------
# Database Schema
# -----------------------------------------

SCHEMA = """
Table: employees

Columns:
id (integer)
name (varchar)
department (varchar)
salary (integer)
"""


# -----------------------------------------
# SQL Query Generator
# -----------------------------------------


def generate_sql(user_query: str):

    prompt = f"""
    You are an expert PostgreSQL query generator.

    Database Schema:
    {SCHEMA}

    Convert the user question into a VALID PostgreSQL query.

    Rules:
ONLY generate SQL
NO markdown
NO explanations
NO backticks
PostgreSQL syntax only

    User Question:
    {user_query}
    """

    response = llm.invoke(prompt)

    sql_query = response.content.strip()

    # remove accidental markdown
    sql_query = sql_query.replace("```sql", "")
    sql_query = sql_query.replace("```", "")

    return sql_query.strip()


# -----------------------------------------
# Execute SQL
# -----------------------------------------


def execute_sql(query: str):

    with engine.connect() as conn:

        result = conn.execute(text(query))

        rows = result.fetchall()

    return rows


# -----------------------------------------
# Main SQL Agent
# -----------------------------------------


def run_sql_query(user_query: str):

    try:

        sql_query = generate_sql(user_query)

        print("\nGenerated SQL:")
        print(sql_query)

        rows = execute_sql(sql_query)

        if not rows:
            return "No results found."

        return str(rows)

    except Exception as e:

        return f"SQL Error: {str(e)}"
