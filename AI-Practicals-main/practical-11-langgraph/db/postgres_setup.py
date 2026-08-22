# ==========================================
# 1. IMPORTS SECTION
# ==========================================

# Import 'create_engine' (to set up the database connection) and 'text' (to format raw SQL strings) 
# from the SQLAlchemy library, which is a popular SQL toolkit for Python.
# Import Python's built-in 'os' module to interact with the operating system, 
# specifically to fetch the environment variables we just loaded.
import os

# Import 'load_dotenv' from the python-dotenv library. 
# This is used to read sensitive variables (like passwords or URLs) from a local '.env' file.
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# ==========================================
# 2. CONFIGURATION & SETUP
# ==========================================

# Execute the function to look for a file named '.env' in the same folder.
# It reads the variables inside that file and loads them into the system environment.
load_dotenv()

# Retrieve the specific environment variable named "DATABASE_URL".
# This string tells the program where the database is and how to log in 
# (e.g., "postgresql://username:password@localhost:5432/mydatabase").
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy "engine". 
# The engine is the core interface to the database. It manages the connection pool 
# and translates our Python commands into a language the specific database understands.
engine = create_engine(DATABASE_URL)


# ==========================================
# 3. SQL QUERY DEFINITION
# ==========================================

# Define a multi-line string containing standard SQL code.
# 'CREATE TABLE IF NOT EXISTS' ensures we don't get an error if the table is already there.
# It creates an 'employees' table with 4 columns: id, name, department, and salary.
query = """
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(100),
    salary INTEGER
);
"""


# ==========================================
# 4. DATABASE EXECUTION
# ==========================================

# Open a connection to the database using a 'with' block (a Context Manager).
# Using 'with' is a best practice because it automatically safely closes the 
# database connection ('conn') when the indented code finishes running, even if it crashes.
with engine.connect() as conn:
    
    # Execute the SQL command. 
    # We must wrap our string 'query' in SQLAlchemy's 'text()' function 
    # so the engine recognizes it as a legitimate, executable SQL command.
    conn.execute(text(query))
    
    # Save (commit) the changes to the database. 
    # By default in SQLAlchemy 2.0+, queries are run in a transaction. 
    # If we don't explicitly commit, the table creation will be rolled back (undone) when the connection closes.
    conn.commit()

# Print a success message to the console to let the user know the script finished without errors.
print("Employees table created successfully.")