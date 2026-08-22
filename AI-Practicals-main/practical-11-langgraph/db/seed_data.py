# ==========================================
# 1. IMPORTS SECTION
# ==========================================

# Import built-in Python modules.
# 'os' is used to interact with the operating system (to get environment variables).
# 'random' is used to generate random numbers and make random selections from lists.
import os
import random

# Import 'load_dotenv' to securely read configuration variables from a local '.env' file.
from dotenv import load_dotenv

# Import 'Faker' from the faker library.
# Faker is a tool used to automatically generate realistic-looking fake data (names, addresses, emails, etc.).
from faker import Faker

# Import 'create_engine' to build the database connection bridge,
# and 'text' to safely format raw SQL strings for SQLAlchemy to execute.
from sqlalchemy import create_engine, text

# ==========================================
# 2. CONFIGURATION & SETUP
# ==========================================

# Read the '.env' file and load its contents into the system's environment variables.
load_dotenv()

# Create an instance (object) of the Faker class.
# We will use this 'fake' object later to generate random employee names.
fake = Faker()

# Fetch the database connection string (e.g., "postgresql://user:pass@localhost/db")
# that was just loaded into the environment by dotenv.
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy "engine", which manages the actual connection to your database.
engine = create_engine(DATABASE_URL)

# Define a standard Python list containing different department names.
# We will randomly assign employees to one of these departments.
departments = ["Engineering", "Finance", "HR", "Sales", "Marketing"]


# ==========================================
# 3. DATABASE EXECUTION & DATA GENERATION
# ==========================================

# Open a connection to the database safely using a Context Manager ('with' statement).
# This ensures the connection ('conn') is automatically closed when we are done.
with engine.connect() as conn:

    # Start a loop that will run exactly 50 times.
    # The underscore '_' is a standard Python convention meaning "we need a loop to run this many times,
    # but we don't actually care about the loop number itself (0, 1, 2, etc.)".
    for _ in range(50):

        # Define the SQL command to insert a new row into the 'employees' table.
        # Notice the `:name`, `:department`, and `:salary`. These are "named parameters" (placeholders).
        # We use placeholders instead of directly injecting Python strings into SQL to prevent
        # syntax errors and protect against SQL Injection attacks.
        insert_query = text("""
        INSERT INTO employees (name, department, salary)
        VALUES (:name, :department, :salary)
        """)

        # Execute the SQL query for this specific loop iteration.
        # We pass the 'insert_query' and a dictionary containing the actual values for our placeholders.
        conn.execute(
            insert_query,
            {
                # fake.name() generates a random, realistic full name (e.g., "John Doe").
                "name": fake.name(),
                # random.choice() picks one random item from our 'departments' list.
                "department": random.choice(departments),
                # random.randint() generates a random integer between 30,000 and 150,000.
                "salary": random.randint(30000, 150000),
            },
        )

    # After the loop finishes running 50 times, we save (commit) all the changes to the database at once.
    # If we don't call commit(), none of the 50 inserted rows will be saved when the connection closes.
    conn.commit()

# Print a success message to the console to let the user know the script finished successfully.
print("Dummy data inserted successfully.")
