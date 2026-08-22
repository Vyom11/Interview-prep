# SQL, PostgreSQL, and DBMS Cheat Sheet (Senior Engineer Edition)

## Database Management Commands

### 1. CREATE DATABASE: Create a New Database
```sql
CREATE DATABASE company;
```
This command creates a new [database](https://www.geeksforgeeks.org/dbms/what-is-database/) named "company."

### 2. USE: Select a Specific Database to Work With
```sql
USE company;
```
This command selects the database named "company" for further operations.

### 3. ALTER DATABASE: Modify a Database's Attributes
```sql
ALTER DATABASE database_name
```

### 4. DROP DATABASE: Delete an Existing Database
```sql
DROP DATABASE company;
```
This command deletes the database named "company" and all its associated data.

### 5. CREATE: Create a New Table, Database or Index
```sql
CREATE TABLE employees (
  employee_id INT PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  department VARCHAR(50),
  salary DECIMAL(10, 2)
);
```
This command creates a table named "employees" with columns for employee ID, first name, last name, department, and salary. The `employee_id` column is set as the primary key.

### 6. INSERT INTO: Add New Records To A Table
```sql
INSERT INTO employees (employee_id, first_name, last_name, department, salary)
VALUES
  (1, 'John', 'Doe', 'HR', 50000.00),
  (2, 'Jane', 'Smith', 'IT', 60000.00),
  (3, 'Alice', 'Johnson', 'Finance', 55000.00),
  (4, 'Bob', 'Williams', 'IT', 62000.00),
  (5, 'Emily', 'Brown', 'HR', 48000.00);
```
This command inserts sample data into the "employees" table with values for employee ID, first name, last name, department, and salary.

### 7. ALTER TABLE: Modify An Existing Table's Structure
```sql
ALTER TABLE employees
ADD COLUMN new_column INT;
```
This command adds a new column named "new_column" of integer type to the existing "employees" table.

### 8. DROP TABLE: Delete A Table And Its Data
```sql
DROP TABLE employees;
```
This command deletes the entire "employees" table along with all its data.

---

## Reading/Querying Data in SQL

Explore this section to get the cheat sheet on how to use SELECT, DISTINCT, and other querying data in SQL.

### 9. SELECT: Retrieve Data From One Or More Tables
```sql
SELECT * FROM employees;
```
This query will retrieve all columns from the employees table.

### 10. DISTINCT: Select Unique Values From A Column
```sql
SELECT DISTINCT department FROM employees;
```
This query will return unique department names from the employees table.

### 11. WHERE: Filter Rows Based On Specified Conditions
```sql
SELECT * FROM employees WHERE salary > 55000.00;
```
This query will return employees whose salary is greater than 55000.00.

### 12. LIMIT: Limit The Number Of Rows Returned In The Result Set
```sql
SELECT * FROM employees LIMIT 3;
```
This query will limit the result set to the first 3 rows.

### 13. OFFSET: Skip A Specified Number Of Rows Before Returning The Result Set
```sql
SELECT * FROM employees LIMIT 10000 OFFSET 2;
```
This query retrieves all rows from the "employees" table, skipping the first 2 rows and limiting the result to 10,000 rows.

### 14. FETCH: Retrieve A Specified Number Of Rows From The Result Set
```sql
SELECT * FROM employees FETCH FIRST 3 ROWS ONLY;
```
This query will fetch the first 3 rows from the result set.

### 15. CASE: Perform Conditional Logic In A Query
```sql
SELECT
  first_name,
  last_name,
  CASE
    WHEN salary > 55000 THEN 'High'
    WHEN salary > 50000 THEN 'Medium'
    ELSE 'Low'
  END AS salary_category
FROM employees;
```
This query will categorize employees based on their salary into 'High', 'Medium', or 'Low'.

### 16. UPDATE: Modify Existing Records In A Table
```sql
UPDATE employees
SET salary = 55000.00
WHERE employee_id = 1;
```
This query will update the salary of the employee with `employee_id` 1 to 55000.00.

---

## Deleting Data in SQL

### 17. DELETE: Remove Records From A Table
```sql
DELETE FROM employees
WHERE employee_id = 5;
```
This query will delete the record of the employee with `employee_id` 5 from the employees table.

---

## Filtering Data in SQL

### 18. WHERE: Filter Rows Based On Specified Conditions
```sql
SELECT * FROM employees
WHERE department = 'IT';
```
This query will retrieve all employees who work in the IT department.

### 19. LIKE: Match A Pattern In A Column
```sql
SELECT * FROM employees
WHERE first_name LIKE 'J%';
```
This query will retrieve all employees whose first name starts with 'J'.

### 20. IN: Match Any Value In A List
```sql
SELECT * FROM employees
WHERE department IN ('HR', 'Finance');
```
This query will retrieve all employees who work in the HR or Finance departments.

### 21. BETWEEN: Match Values Within A Specified Range
```sql
SELECT * FROM employees
WHERE salary BETWEEN 50000 AND 60000;
```
This query will retrieve all employees whose salary is between 50000 and 60000.

### 22. IS NULL: Match NULL Values
```sql
SELECT * FROM employees
WHERE department IS NULL;
```
This query will retrieve all employees where the department is not assigned (NULL).

### 23. ORDER BY: Sort The Result Set
```sql
SELECT * FROM employees
ORDER BY salary DESC;
```
This query will retrieve all employees sorted by salary in descending order.

### 24. AND: Combines Multiple Conditions In A WHERE Clause
```sql
SELECT * FROM employees
WHERE department = 'IT' AND salary > 60000;
```
This query will retrieve employees who work in the IT department and have a salary greater than 60000.

### 25. OR: Specifies Multiple Conditions Where Any One Of Them Should Be True
```sql
SELECT * FROM employees
WHERE department = 'HR' OR department = 'Finance';
```
This query will retrieve employees who work in either the HR or Finance department.

### 26. NOT: Negates A Condition
```sql
SELECT * FROM employees
WHERE NOT department = 'IT';
```
This query will retrieve employees who do not work in the IT department.

### 27. LIKE: Searches For A Specified Pattern In A Column
```sql
SELECT * FROM employees
WHERE first_name LIKE 'J%';
```
This query will retrieve employees whose first name starts with 'J'.

### 28. IN: Checks If A Value Matches Any Value In
```sql
SELECT * FROM employees
WHERE department IN ('HR', 'Finance');
```
This query will retrieve employees who work in the HR or Finance departments.

### 29. BETWEEN: Selects Values Within a Specified Range
```sql
SELECT * FROM employees
WHERE salary BETWEEN 50000 AND 60000;
```
This query will retrieve employees whose salary is between 50000 and 60000.

### 30. IS NULL: Checks if a Value is NULL
```sql
SELECT * FROM employees
WHERE department IS NULL;
```
This query will retrieve employees where the department is not assigned (NULL).

### 31. ORDER BY: Sorts the Result Set in Ascending or Descending Order
```sql
SELECT * FROM employees
ORDER BY salary DESC;
```
This query will retrieve all employees sorted by salary in descending order.

### 32. GROUP BY: Groups Rows that have the Same Values into Summary Rows
```sql
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department;
```
This query will group employees by department and count the number of employees in each department.

### 33. COUNT: Count The Number Of Rows In A Result Set
```sql
SELECT COUNT(*) FROM employees;
```
This query will count the total number of employees.

### 34. SUM: Calculate The Sum Of Values In A Column
```sql
SELECT SUM(salary) FROM employees;
```
This query will calculate the total salary of all employees.

### 35. AVG: Calculate The Average Value Of A Column
```sql
SELECT AVG(salary) FROM employees;
```
This query will calculate the average salary of all employees.

### 36. MIN: Find the Minimum Value in a Column
```sql
SELECT MIN(salary) FROM employees;
```
This query will find the minimum salary among all employees.

### 37. MAX: Find the Maximum Value in a Column
```sql
SELECT MAX(salary) FROM employees;
```
This query will find the maximum salary among all employees.

### 38. GROUP BY: Group Rows Based on a Specified Column
```sql
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department;
```
This query will group employees by department and count the number of employees in each department.

### 39. HAVING: Filter Groups Based on Specified Conditions
```sql
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 55000;
```
This query will calculate the average salary for each department and return only those departments where the average salary is greater than 55000.

---

## SQL Constraints

### 40. PRIMARY KEY: Uniquely Identifies Each Record in a Table
```sql
CREATE TABLE employees (
  employee_id INT PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50)
);
```
`employee_id` is designated as the [primary key](https://www.geeksforgeeks.org/dbms/primary-key-in-dbms/), ensuring that each employee record has a unique identifier.

### 41. FOREIGN KEY: Establishes a Relationship Between Two Tables
```sql
CREATE TABLE departments (
  department_id INT PRIMARY KEY,
  department_name VARCHAR(50)
);

CREATE TABLE employees (
  employee_id INT PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  department_id INT,
  FOREIGN KEY (department_id) REFERENCES departments(department_id)
);
```
`department_id` column in the employees table is a foreign key that references the `department_id` column in the departments table, establishing a relationship between the two tables.

### 42. UNIQUE: Ensures That All Values in a Column Are Unique
```sql
CREATE TABLE employees (
  employee_id INT PRIMARY KEY,
  email VARCHAR(100) UNIQUE
);
```
`email` column must contain unique values for each employee.

### 43. NOT NULL: Ensures That a Column Does Not Contain NULL Values
```sql
CREATE TABLE employees (
  employee_id INT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL
);
```
`first_name` and `last_name` columns must have values and cannot be NULL.

### 44. CHECK: Specifies a Condition That Must Be Met for a Column's Value
```sql
CREATE TABLE employees (
  employee_id INT PRIMARY KEY,
  age INT CHECK (age >= 18)
);
```
`age` column must have a value of 18 or greater due to the CHECK constraint.

---

## SQL Joins

### 45. INNER JOIN: Retrieves Records That Have Matching Values in Both Tables
```sql
SELECT * FROM employees
INNER JOIN departments ON employees.department_id = departments.department_id;
```
This query will retrieve records from both the employees and departments tables where there is a match on the `department_id` column.

### 46. LEFT JOIN: Retrieves All Records from the Left Table and the Matched Records from the Right Table
```sql
SELECT * FROM employees
LEFT JOIN departments ON employees.department_id = departments.department_id;
```
This query will retrieve all records from the employees table and only the matching records from the departments table.

### 47. RIGHT JOIN: Retrieves All Records from the Right Table and the Matched Records from the Left Table
```sql
SELECT * FROM employees
RIGHT JOIN departments ON employees.department_id = departments.department_id;
```
This query will retrieve all records from the departments table and only the matching records from the employees table.

### 48. FULL OUTER JOIN: Retrieves All Records When There Is a Match in Either the Left or Right Table
```sql
SELECT * FROM employees
FULL OUTER JOIN departments ON employees.department_id = departments.department_id;
```
This query will retrieve all records from both the employees and departments tables, including unmatched records.

### 49. CROSS JOIN: Retrieves the Cartesian Product of the Two Tables
```sql
SELECT * FROM employees
CROSS JOIN departments;
```
This query will retrieve all possible combinations of records from the employees and departments tables.

### 50. SELF JOIN: Joins a Table to Itself
```sql
SELECT e1.first_name, e2.first_name
FROM employees e1, employees e2
WHERE e1.employee_id = e2.manager_id;
```
In this example, the employees table is joined to itself to find employees and their respective managers based on the `manager_id` column.

---

## SQL Functions

### 51. Scalar Functions: Functions That Return a Single Value
```sql
SELECT UPPER(first_name) AS upper_case_name FROM employees;
```
This query uses the `UPPER()` scalar function to convert the `first_name` column values to uppercase.

### 52. Aggregate Functions: Functions That Operate on a Set of Values and Return a Single Value
```sql
SELECT AVG(salary) AS average_salary FROM employees;
```
This query uses the `AVG()` aggregate function to calculate the average salary of all employees.

### 53. String Functions: Functions That Manipulate String Values

**CONCAT:**
```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employees;
```
This query uses the `CONCAT()` string function to concatenate the `first_name` and `last_name` columns into a single column called `full_name`.

**SUBSTR:**
```sql
SELECT SUBSTR(first_name, 1, 3) AS short_name FROM employees;
```
This query uses the `SUBSTR()` function to extract the first three characters of the `first_name` column for each employee. The result is displayed in a new column called `short_name`.

**INSERT:**
```sql
SELECT INSERT(full_name, 6, 0, 'Amazing ') AS modified_name
FROM (SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employees) AS employee_names;
```
This query first concatenates the `first_name` and `last_name` columns into a single column called `full_name`. Then, it uses the `INSERT()` function to insert the string 'Amazing ' at the 6th position of the `full_name` column for each employee. The modified names are displayed in a new column called `modified_name`.

### 54. Date and Time Functions: Functions That Operate on Date and Time Values
```sql
SELECT CURRENT_DATE AS current_date FROM dual;
```
This query uses the `CURRENT_DATE` date function to retrieve the current date.

### 55. Mathematical Functions: Functions That Perform Mathematical Operations
```sql
SELECT SQRT(25) AS square_root FROM dual;
```
This query uses the `SQRT()` mathematical function to calculate the square root of 25.

---

## Window Functions (Advanced)

Window functions allow you to perform calculations across a set of rows that are related to the current row.

### 56. ROW_NUMBER: Assigns a Unique Number to Each Row
```sql
SELECT 
  employee_id,
  first_name,
  salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC) AS salary_rank
FROM employees;
```
This query assigns a unique number to each employee based on their salary in descending order.

### 57. RANK and DENSE_RANK: Rank Rows with Handling for Ties
```sql
SELECT 
  employee_id,
  first_name,
  salary,
  RANK() OVER (ORDER BY salary DESC) AS rank,
  DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank
FROM employees;
```
`RANK()` leaves gaps in numbering after ties, while `DENSE_RANK()` does not.

### 58. LAG and LEAD: Access Previous and Next Row Values
```sql
SELECT 
  employee_id,
  first_name,
  salary,
  LAG(salary) OVER (ORDER BY salary DESC) AS prev_salary,
  LEAD(salary) OVER (ORDER BY salary DESC) AS next_salary
FROM employees;
```
This query retrieves the previous and next employee's salary for comparison.

### 59. SUM and AVG over Window: Running Totals and Moving Averages
```sql
SELECT 
  employee_id,
  first_name,
  salary,
  SUM(salary) OVER (ORDER BY employee_id) AS running_total,
  AVG(salary) OVER (ORDER BY employee_id ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS moving_avg
FROM employees;
```
This creates a running total of salaries and a moving average across a window of 3 rows.

---

## Subqueries in SQL

This SQL cheat sheet explains how to nest queries for powerful data filtering and manipulation within a single statement.

### 60. Single-row Subquery: Returns One Row of Result
```sql
SELECT first_name, last_name
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);
```
In this example, the [subquery](https://www.geeksforgeeks.org/sql/sql-subquery/)([SELECT](https://www.geeksforgeeks.org/sql/sql-select-query/) [MAX](https://www.geeksforgeeks.org/sql/sql-min-and-max/)(salary) FROM employees) returns a single row containing the maximum salary, and it's used to filter employees who have the maximum salary.

### 61. Multiple-row Subquery: Returns Multiple Rows of Result
```sql
SELECT department_name
FROM departments
WHERE department_id IN (SELECT department_id FROM employees);
```
In this example, the subquery `(SELECT department_id FROM employees)` returns multiple rows containing department IDs, and it's used to filter department names based on those IDs.

### 62. Correlated Subquery: References a Column from the Outer Query
```sql
SELECT first_name, last_name
FROM employees e
WHERE salary > (SELECT AVG(salary) FROM employees WHERE department = e.department);
```
In this example, the subquery `(SELECT [AVG](https://www.geeksforgeeks.org/sql/sql-count-avg-and-sum/)(salary) FROM employees [WHERE](https://www.geeksforgeeks.org/sql/sql-where-clause/) department = e.department)` is correlated with the outer query by referencing the `department` column from the outer query. It calculates the average salary for each department and is used to filter employees whose salary is greater than the average salary of their respective department.

### 63. Nested Subquery: A Subquery Inside Another Subquery
```sql
SELECT first_name, last_name
FROM employees
WHERE department_id IN (
   SELECT department_id
   FROM departments
   WHERE department_name = 'IT'
);
```
In this example, the subquery `(SELECT department_id FROM departments WHERE department_name = 'IT')` is nested within the outer query. It retrieves the department ID for the IT department, which is then used in the outer query to filter employees belonging to the IT department.

---

## Views, Indexes, and Transactions

### 64. CREATE VIEW: Create a Virtual Table Based on the Result of a SELECT Query
```sql
CREATE VIEW high_paid_employees AS
SELECT *
FROM employees
WHERE salary > 60000;
```
This query creates a [views](https://www.geeksforgeeks.org/sql/sql-views/) named `high_paid_employees` that contains all employees with a salary greater than 60000.

### 65. DROP VIEW: Delete a View
```sql
DROP VIEW IF EXISTS high_paid_employees;
```
This query drops the `high_paid_employees` view if it exists.

### 66. CREATE MATERIALIZED VIEW (PostgreSQL): Create a Physical Copy of Query Results
```sql
CREATE MATERIALIZED VIEW high_paid_employees_mat AS
SELECT *
FROM employees
WHERE salary > 60000;

-- To refresh the materialized view
REFRESH MATERIALIZED VIEW high_paid_employees_mat;
```
Unlike regular views, materialized views store the result set physically on disk, providing faster query performance at the cost of manual refresh operations.

### 67. CREATE INDEX: Create an Index on a Table
```sql
CREATE INDEX idx_department ON employees (department);

-- Create a partial index (PostgreSQL-specific)
CREATE INDEX idx_high_salary ON employees(salary) 
WHERE salary > 60000;

-- Create a multi-column index
CREATE INDEX idx_dept_salary ON employees(department, salary);
```
This query creates an [index](https://www.geeksforgeeks.org/sql/sql-indexes/) named `idx_department` on the `department` column of the employees table. Partial and multi-column indexes are PostgreSQL-specific optimizations.

### 68. DROP INDEX: Remove an Index
```sql
DROP INDEX IF EXISTS idx_department;
```
This query drops the `idx_department` index if it exists.

### 69. BEGIN TRANSACTION: Start a New Transaction
```sql
BEGIN TRANSACTION;
```
This statement starts a new [transaction](https://www.geeksforgeeks.org/sql/sql-transactions/).

### 70. COMMIT: Save Changes Made During the Current Transaction
```sql
COMMIT;
```
This statement saves all changes made during the current [transaction](https://www.geeksforgeeks.org/sql/sql-transactions/).

### 71. ROLLBACK: Undo Changes Made During the Current Transaction
```sql
ROLLBACK;
```
This statement undoes all changes made during the current transaction.

### 72. SAVEPOINT: Create a Point Within a Transaction to Rollback To
```sql
BEGIN;
INSERT INTO employees VALUES (6, 'Charlie', 'Davis', 'IT', 65000);
SAVEPOINT sp1;
INSERT INTO employees VALUES (7, 'Diana', 'Evans', 'HR', 52000);
ROLLBACK TO sp1;
COMMIT;
```
This saves the first insert but rolls back the second insert, using a savepoint for fine-grained transaction control.

---

## Advanced SQL Features

### 73. Stored Procedures: Precompiled SQL Statements That Can Be Executed with a Single Command
```sql
CREATE PROCEDURE get_employee_count()
BEGIN
  SELECT COUNT(*) FROM employees;
END;
```
This query creates a [stored procedure](https://www.geeksforgeeks.org/sql/what-is-stored-procedures-in-sql/) named `get_employee_count` that returns the count of employees.

### 74. Triggers: Automatically Execute a Set of SQL Statements When a Specified Event Occurs
```sql
CREATE TRIGGER before_employee_insert
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
  SET NEW.creation_date = NOW();
END;
```
This query creates a [trigger](https://www.geeksforgeeks.org/sql/sql-trigger-student-database/) named `before_employee_insert` that sets the `creation_date` column to the current date and time before inserting a new employee record.

### 75. User-defined Functions (UDFs): Custom SQL Functions Created by Users to Perform Specific Tasks
```sql
CREATE FUNCTION calculate_bonus(salary DECIMAL) RETURNS DECIMAL
BEGIN
  RETURN salary * 0.1; -- 10% bonus
END;
```
This query creates a user-defined function named `calculate_bonus` that calculates the bonus based on the salary.

### 76. Common Table Expressions (CTEs): Temporary Result Sets That Can Be Referenced Within a SELECT, INSERT, UPDATE, or DELETE Statement
```sql
WITH high_paid_employees AS (
  SELECT * FROM employees WHERE salary > 60000
)
SELECT * FROM high_paid_employees;
```
This query uses a [common table expression](https://www.geeksforgeeks.org/sql/cte-in-sql/) named `high_paid_employees` to retrieve all employees with a salary greater than 60000.

### 77. Recursive CTEs: CTEs That Reference Themselves
```sql
WITH RECURSIVE org_hierarchy AS (
  -- Base case: get employees with no manager
  SELECT employee_id, first_name, manager_id, 1 AS level
  FROM employees
  WHERE manager_id IS NULL
  UNION ALL
  -- Recursive case: get employees under each manager
  SELECT e.employee_id, e.first_name, e.manager_id, oh.level + 1
  FROM employees e
  INNER JOIN org_hierarchy oh ON e.manager_id = oh.employee_id
)
SELECT * FROM org_hierarchy;
```
This creates a hierarchical view of the organization by recursively joining employees to their managers.

---

## Query Execution & Optimization

Understanding how PostgreSQL executes queries is crucial for optimization at scale.

### 78. EXPLAIN: View the Query Execution Plan
```sql
EXPLAIN SELECT * FROM employees WHERE salary > 60000;
```
Output shows:
```
Seq Scan on employees  (cost=0.00..35.50 rows=2 width=100)
  Filter: (salary > 60000)
```

### 79. EXPLAIN ANALYZE: Execute the Query and Show Actual Performance Metrics
```sql
EXPLAIN ANALYZE SELECT * FROM employees WHERE salary > 60000;
```
Output includes:
```
Seq Scan on employees  (cost=0.00..35.50 rows=2 width=100) 
  (actual time=0.012..0.015 rows=2 loops=1)
  Filter: (salary > 60000)
```

### 80. Sequential Scans vs. Index Scans: Understanding Plan Selection

**Sequential Scan (Full Table Scan):**
```sql
EXPLAIN SELECT * FROM employees WHERE first_name = 'John';
```
When there's no index or filtering returns a large portion of rows.

**Index Scan:**
```sql
EXPLAIN SELECT * FROM employees WHERE employee_id = 5;
```
When an index exists on the column and returns a small result set.

**Key Metrics in EXPLAIN ANALYZE:**
- **cost**: Planning estimate of execution time (not actual)
- **rows**: Expected number of rows output
- **actual time**: Real wall-clock time (in milliseconds)
- **loops**: Number of times node is executed

### 81. Improving Query Performance: Common Optimization Techniques

**1. Using LIMIT to reduce output:**
```sql
EXPLAIN ANALYZE SELECT * FROM employees ORDER BY salary DESC LIMIT 10;
```

**2. Creating indexes on frequently filtered columns:**
```sql
CREATE INDEX idx_salary ON employees(salary);
EXPLAIN ANALYZE SELECT * FROM employees WHERE salary > 60000;
```

**3. Using ANALYZE to update table statistics:**
```sql
ANALYZE employees;
```

**4. Avoiding functions in WHERE clauses (prevents index usage):**
```sql
-- Bad: Function prevents index usage
SELECT * FROM employees WHERE UPPER(first_name) = 'JOHN';

-- Good: Use indexed column directly
SELECT * FROM employees WHERE first_name = 'John';
```

**5. Using appropriate data types:**
```sql
-- Bad: String comparison slower than numeric
SELECT * FROM employees WHERE employee_id = '5';

-- Good: Numeric comparison
SELECT * FROM employees WHERE employee_id = 5;
```

---

## Transaction Isolation Levels

Transaction isolation levels define how transactions interact with each other and what anomalies they prevent.

### 82. Read Uncommitted (Isolation Level 0)

**Definition**: A transaction can read data that has been modified but not yet committed by another transaction.

**Anomalies Prevented**: None

**Anomalies Allowed**:
- Dirty Reads
- Non-repeatable Reads
- Phantom Reads

```sql
-- Set isolation level in PostgreSQL
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN;
SELECT * FROM employees WHERE employee_id = 1;
COMMIT;
```

**Warning**: Rarely used in production; compromises data integrity.

### 83. Read Committed (Isolation Level 1)

**Definition**: A transaction only sees data that has been committed before the transaction began or that was committed after the transaction began. This is the default level in most databases.

**Anomalies Prevented**: Dirty Reads

**Anomalies Allowed**:
- Non-repeatable Reads
- Phantom Reads

```sql
-- PostgreSQL default
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
  SELECT salary FROM employees WHERE employee_id = 1; -- might change if modified elsewhere
  COMMIT;
```

**Use Case**: Most OLTP systems; good balance between consistency and concurrency.

### 84. Repeatable Read (Isolation Level 2)

**Definition**: Within a transaction, all reads of the same data return the same result, even if other transactions modify the data.

**Anomalies Prevented**:
- Dirty Reads
- Non-repeatable Reads

**Anomalies Allowed**:
- Phantom Reads

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
  SELECT COUNT(*) FROM employees WHERE department = 'IT';
  -- Other transactions can INSERT new IT employees
  SELECT COUNT(*) FROM employees WHERE department = 'IT'; -- Might return different count
COMMIT;
```

**Use Case**: Scenarios where consistency within a transaction is critical.

### 85. Serializable (Isolation Level 3)

**Definition**: The highest isolation level; provides complete isolation. Transactions are executed as if they were serialized (one after another).

**Anomalies Prevented**:
- Dirty Reads
- Non-repeatable Reads
- Phantom Reads

**Trade-off**: Lowest concurrency performance.

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
  SELECT COUNT(*) FROM employees WHERE department = 'IT';
  SELECT COUNT(*) FROM employees WHERE department = 'IT'; -- Always same count
COMMIT;
```

**Use Case**: Financial transactions, critical reports requiring absolute consistency.

### 86. Isolation Level Comparison Table

| Level | Dirty Reads | Non-repeatable Reads | Phantom Reads | Concurrency |
|-------|-------------|----------------------|---------------|-------------|
| Read Uncommitted | ✓ | ✓ | ✓ | Highest |
| Read Committed | ✗ | ✓ | ✓ | High |
| Repeatable Read | ✗ | ✗ | ✓ | Medium |
| Serializable | ✗ | ✗ | ✗ | Lowest |

### 87. Setting Isolation Level for Specific Transactions

```sql
-- PostgreSQL: Set for entire session
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Set for specific transaction
START TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT * FROM accounts WHERE id = 100;
UPDATE accounts SET balance = balance - 100 WHERE id = 100;
COMMIT;
```

---

## Concurrency Mechanisms

Databases use sophisticated mechanisms to handle multiple concurrent transactions safely.

### 88. Multi-Version Concurrency Control (MVCC)

**Definition**: MVCC allows multiple transactions to read data simultaneously without blocking writes. Each transaction sees a consistent snapshot of the database at a point in time.

**How MVCC Works in PostgreSQL:**

1. **Version Tags**: Each row has transaction ID (xid) tags: `xmin` (created) and `xmax` (deleted)
2. **Snapshot Creation**: When a transaction starts, it captures the current state of committed transactions
3. **Visibility Rules**: A row is visible to a transaction if:
   - `xmin` is committed and <= current transaction's id
   - `xmax` is NULL or not committed or > current transaction's id

**Example:**
```sql
-- Transaction 1
BEGIN;
SELECT * FROM employees WHERE id = 1; -- Returns current version
-- Meanwhile, another transaction updates the row

-- Transaction 1
SELECT * FROM employees WHERE id = 1; -- Still returns same version (MVCC)
COMMIT;
```

**Advantages**:
- Readers don't block writers
- Writers don't block readers
- Better concurrency than traditional locking

**Disadvantages**:
- Requires periodic cleanup (VACUUM) to remove dead rows
- Can cause table bloat if VACUUM isn't run frequently

### 89. Understanding Transactions and MVCC

```sql
-- Create test table
CREATE TABLE accounts (id INT PRIMARY KEY, balance INT);
INSERT INTO accounts VALUES (1, 1000);

-- Transaction A
BEGIN;
SELECT balance FROM accounts WHERE id = 1; -- sees 1000

-- In another session: Transaction B makes a change and commits
UPDATE accounts SET balance = 900 WHERE id = 1;
COMMIT;

-- Back in Transaction A
SELECT balance FROM accounts WHERE id = 1; 
-- Depending on isolation level:
-- READ COMMITTED: sees 900 (newer version)
-- REPEATABLE READ: sees 1000 (original snapshot)
COMMIT;
```

### 90. Deadlocks: Definition and Detection

**Definition**: A deadlock occurs when two or more transactions wait for each other to release locks, creating a circular dependency.

**Classic Deadlock Scenario:**

```sql
-- Session 1
BEGIN;
UPDATE employees SET salary = 60000 WHERE id = 1;
-- ... waiting for lock on id = 2
UPDATE employees SET salary = 70000 WHERE id = 2;
COMMIT;

-- Session 2 (runs concurrently)
BEGIN;
UPDATE employees SET salary = 65000 WHERE id = 2;
-- ... waiting for lock on id = 1
UPDATE employees SET salary = 75000 WHERE id = 1;
COMMIT;
```

**Error**: `ERROR: deadlock detected`

### 91. Deadlock Prevention and Resolution Strategies

**1. Lock Ordering: Acquire locks in a consistent order**
```sql
-- Always lock in order: id ascending
BEGIN;
UPDATE employees SET salary = 60000 WHERE id = 1;
UPDATE employees SET salary = 70000 WHERE id = 2;
COMMIT;
```

**2. Use Shorter Transactions**
```sql
-- Good: Fast, focused transaction
BEGIN;
UPDATE employees SET salary = 60000 WHERE id = 1;
COMMIT;

BEGIN;
UPDATE employees SET salary = 70000 WHERE id = 2;
COMMIT;
```

**3. Set Appropriate Isolation Levels**
```sql
-- Use READ COMMITTED when possible to reduce lock contention
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

**4. Automatic Deadlock Detection**
```sql
-- PostgreSQL automatically detects and reports deadlocks
-- Application should implement retry logic
```

**5. Retry Logic in Application Code**
```python
# Pseudocode for handling deadlocks
max_retries = 3
for attempt in range(max_retries):
    try:
        db.execute_transaction(sql)
        break
    except DeadlockError:
        if attempt < max_retries - 1:
            time.sleep(random.uniform(0.1, 1.0))  # Exponential backoff
        else:
            raise
```

### 92. Lock Types in PostgreSQL

**Access Exclusive Lock** (Most restrictive)
```sql
-- Acquired by: ALTER TABLE, DROP TABLE, TRUNCATE, EXCLUSIVE lock
ALTER TABLE employees ADD COLUMN new_field INT;
```

**Exclusive Lock**
```sql
-- Acquired by: UPDATE, DELETE
UPDATE employees SET salary = 60000 WHERE id = 1;
```

**Share Lock**
```sql
-- Acquired by: SELECT FOR SHARE (explicitly)
SELECT * FROM employees WHERE id = 1 FOR SHARE;
```

**Row-Level Locks** (Most granular)
```sql
-- FOR UPDATE: Exclusive row lock
SELECT * FROM employees WHERE id = 1 FOR UPDATE;

-- FOR SHARE: Share row lock
SELECT * FROM employees WHERE id = 1 FOR SHARE;

-- FOR UPDATE NOWAIT: Fail immediately if row is locked
SELECT * FROM employees WHERE id = 1 FOR UPDATE NOWAIT;
```

---

## Database Scaling Strategies

As data grows, scaling becomes essential. Here are the main approaches:

### 93. Vertical Scaling (Scale Up)

**Definition**: Increasing the capacity of a single database server (more CPU, RAM, storage).

**Advantages**:
- Simpler to implement
- No application changes needed
- No data consistency issues

**Disadvantages**:
- Hardware limits
- Single point of failure
- Expensive at extreme scales
- Causes downtime during upgrades

### 94. Horizontal Scaling: Sharding (Scale Out)

**Definition**: Distributing data across multiple database servers based on a sharding key. Each shard handles a subset of data.

**Sharding Strategy Example:**

```sql
-- Shard based on customer_id (modulo approach)
-- Shard 1: customer_id % 4 = 0
-- Shard 2: customer_id % 4 = 1
-- Shard 3: customer_id % 4 = 2
-- Shard 4: customer_id % 4 = 3

-- Shard 1 Database
CREATE TABLE orders_shard_1 (
  order_id INT,
  customer_id INT,
  amount DECIMAL,
  CHECK (customer_id % 4 = 0)
);

-- Shard 2 Database
CREATE TABLE orders_shard_2 (
  order_id INT,
  customer_id INT,
  amount DECIMAL,
  CHECK (customer_id % 4 = 1)
);
```

**Sharding Key Strategies**:
1. **Range-based**: customer_id 1-1000 on Shard 1, 1001-2000 on Shard 2
2. **Hash-based**: customer_id % number_of_shards
3. **Geographic**: Shard based on region
4. **Directory-based**: Lookup table maps shard key to shard

**Challenges**:
- Complex application logic
- Difficult joins across shards
- Data redistribution (resharding) is complex
- Uneven data distribution (hotspots)

### 95. Horizontal Scaling: Replication

**Definition**: Copying data across multiple servers for redundancy and load distribution.

**Master-Slave (Primary-Replica) Replication:**

```sql
-- Master (PostgreSQL 12+)
CREATE PUBLICATION orders_pub FOR TABLE orders;

-- Slave (Subscriber) - In another database
CREATE SUBSCRIPTION orders_sub CONNECTION 'dbname=mydb host=master_host' 
  PUBLICATION orders_pub;
```

**Characteristics**:
- Master accepts all writes
- Slaves replicate changes from master
- Slaves can serve read-only queries
- Replication lag exists (eventual consistency)

**When to use**:
- Read-heavy workloads
- Disaster recovery
- Geographic distribution of read traffic

**Master-Master (Multi-Master) Replication:**

```sql
-- Both databases act as masters
-- Each can accept writes
-- Changes are replicated to all nodes
-- Requires conflict resolution strategy
```

**Challenges**:
- Write conflicts (different writes to same row)
- Replication lag causes inconsistency
- All nodes must agree on conflicts

**When to use**:
- Multi-region active-active systems
- High availability requirements
- Distributed teams needing local writes

### 96. Connection Pooling: PgBouncer

**Definition**: Maintains a pool of database connections to reduce connection overhead and improve performance.

**Configuration Example (pgbouncer.ini):**
```ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction          # Return conn to pool after each transaction
max_client_conn = 1000           # Max client connections
default_pool_size = 25           # Connections per database per user
reserve_pool_size = 5            # Extra connections for emergencies
reserve_pool_timeout = 3         # Timeout for reserve pool

# Connection limits
max_db_connections = 100         # Max connections to database
max_user_connections = 50        # Max per user
```

**Pool Modes:**
```
session    - One connection per client session (persistent)
transaction - Connection returned to pool after each transaction (default)
statement   - Connection returned after each statement (fastest)
```

**Usage Example:**
```python
import psycopg2

# Connect via PgBouncer (port 6432) instead of direct PostgreSQL (5432)
conn = psycopg2.connect(
    host='localhost',
    port=6432,  # PgBouncer port
    database='mydb',
    user='myuser'
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM employees")
conn.commit()  # Returns connection to pool in transaction mode
conn.close()   # Closes client connection
```

**Benefits**:
- Reduced connection overhead
- Better resource utilization
- Faster query response times
- Protection against connection storms

### 97. Caching Strategies

**Query Result Caching:**

```python
import redis

cache = redis.Redis(host='localhost', port=6379)

def get_employee(emp_id):
    # Check cache first
    cache_key = f"employee:{emp_id}"
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Cache miss: query database
    employee = db.query("SELECT * FROM employees WHERE id = ?", emp_id)
    
    # Store in cache (60 second expiry)
    cache.setex(cache_key, 60, json.dumps(employee))
    return employee
```

**Cache Invalidation Strategies**:
```python
# 1. Time-based expiration (TTL)
cache.setex(key, 300, value)  # 5 minute TTL

# 2. Event-based invalidation
def update_employee(emp_id, new_data):
    db.update("employees", emp_id, new_data)
    cache.delete(f"employee:{emp_id}")  # Invalidate cache

# 3. Pattern-based invalidation
cache.delete_match("employee:*")  # Clear all employee caches
```

---

## CAP Theorem

**Definition**: The CAP Theorem (Brewer's Theorem) states that a distributed system can guarantee at most two of three properties:

### 98. CAP Theorem Components

**Consistency (C)**: Every read receives the most recent write or an error

```
Timeline:
T1: Write X=1 to node A
T2: Read X from node B
Expected: Returns 1 (if replication complete) or error (if not)
NOT acceptable: Returns stale value (0)
```

**Availability (A)**: Every request gets a response (success or failure)

```
If any node fails:
- Available: System responds with cached/local data
- Not Available: System returns error until consistency restored
```

**Partition Tolerance (P)**: System continues despite network partitions (disconnected nodes)

```
Network splits cluster into two groups:
Group 1: Nodes A, B
Group 2: Nodes C, D
Partition Tolerant: Both groups can still operate
Not Partition Tolerant: System stops entirely
```

### 99. CAP Theorem Trade-offs

**CA Systems (Consistency + Availability, No Partition Tolerance)**
- Example: Traditional SQL databases without replication
- Fails when network partition occurs
- Not suitable for distributed systems

```
Scenario: Two-node database, network splits
Node A stays up, Node B disconnects
CA system: Stops accepting writes (sacrifices availability)
```

**CP Systems (Consistency + Partition Tolerance, No Availability)**
- Example: MongoDB, HBase
- When network partition occurs, system becomes unavailable to ensure consistency
- Strong consistency guaranteed

```
Scenario: Distributed MongoDB, network partition
- Primary partition: Continues accepting writes
- Minority partition: Rejects writes (unavailable)
Result: Consistency maintained, availability sacrificed
```

**AP Systems (Availability + Partition Tolerance, No Consistency)**
- Example: Cassandra, DynamoDB, Redis
- During partition, nodes operate independently (eventual consistency)
- Always available but may return stale data

```
Scenario: Cassandra cluster, network partition
- Node A writes X=1
- Network partition occurs
- Node B (in other partition) still accepts writes and reads
- Clients may see X=0 or X=1 (inconsistent)
- After healing: Converges to consistent state
```

### 100. CAP Theorem in Practice

**Example: Banking System (CP - Consistency Priority)**

```python
# PostgreSQL with synchronous replication (CP system)
# Configuration: synchronous_commit = on (wait for replica ACK)

# Write
account.balance -= 100
db.commit()  # Blocks until replica acknowledges

# If network partition:
# - Primary can't confirm write to replica
# - Write is rejected (availability down, consistency up)
```

**Example: Social Media Like Counter (AP - Availability Priority)**

```python
# Cassandra (AP system)
# Write a like without waiting for all replicas

quorum_writes = 1  # Don't wait for majority
def add_like(post_id):
    db.write(f"likes:{post_id}", increment=1, consistency=quorum_writes)
    # Returns immediately, replicas catch up eventually

# During partition: Different replicas may have different counts
# After healing: Replicas merge using Last-Write-Wins
```

### 101. Consistency Models in Distributed Databases

**Strong Consistency (Linearizability)**
```
All operations appear to execute in a total order
Write X=1 -> All subsequent reads see X=1
Cost: Latency (must coordinate across nodes)
```

**Eventual Consistency**
```
After write, all reads eventually see the write
Write X=1 -> Some reads see X=0 (temporarily) -> Eventually all see X=1
Cost: Temporary inconsistency
Benefit: Low latency, high availability
```

**Causal Consistency**
```
If write A causally happens before write B:
All processes see A before B
Used in: DynamoDB, some NoSQL databases
```

**Session Consistency**
```
A single client's reads are consistent
But different clients may see different versions
Used in: Many web applications
```

### 102. Choosing Between CAP Trade-offs

| Use Case | Priority | System | Example |
|----------|----------|--------|---------|
| Financial Transactions | Consistency | CP | PostgreSQL |
| Banking Transfers | Consistency | CP | MySQL |
| Social Media Feeds | Availability | AP | Cassandra |
| Real-time Analytics | Consistency | CP | PostgreSQL |
| Distributed Cache | Availability | AP | Redis |
| IoT Data Ingestion | Availability | AP | Cassandra |
| User Accounts | Consistency | CP | PostgreSQL |
| Product Recommendations | Availability | AP | Cassandra |

---

## DBMS Concepts

## 1) What is DBMS?

A DBMS is software that manages databases, providing an interface to store, retrieve, and manipulate data efficiently and securely.

## 2) What is a Database?

A Database is an organized, consistent, and logical collection of data that can easily be updated, accessed, and managed. Database mostly contains sets of tables or objects which consist of records and fields.

## 3) Explain the difference between a database and a DBMS?

A database is a collection of related data, while a DBMS is software used to manage, store, and retrieve data efficiently from the database.

## 4) Advantages of DBMS over File Systems?

### Data Redundancy and Inconsistency:
Redundancy means repeating the data in a system. In a normal file system, there is a high chance that there can be various files of the same data used by different users for specific purposes. If any user changes the data in its files, then the changes are not reflected in all files. This creates inconsistency in the data, and it may lead to the failure of the system. But in the DBMS, there is only one repository of data, and multiple users can use it. If any user changes the data, then it is reflected to each user as they are using the same repository.

### Data Sharing:
In the normal file system, data sharing is too difficult because file sharing is a complex task. In DBMS, all the data is centralized, so data sharing is a very easy task.

### Data Concurrency:
When more than one user accesses the database simultaneously, then it is called concurrency. In a file system, when multiple users are using the files at the same time, then there may be a chance of anomalies in the data due to changes, and it does not provide any method to detect anomalies. But in DBMS, we have a locking system to detect the anomalies so we can protect the data.

### Data Searching:
To search the data in a file system, we have to write a specific program and run it. In DBMS, we have query languages by which we can write small queries to get the data we want from the database. We can use various query languages, like MySQL, Oracle, etc., for a database to search and retrieve the data.

### Data Integrity:
When we insert new data into the database, we require some specific constraints on the data like integer or not null, etc. The file system does not provide any system to check the constraints, whereas DBMS has the functionality to check the constraints on the data, and it allows user defined data types.

## 5) What is the different languages present in DBMS?

| Language | Full Form | Description | Examples |
|----------|-----------|-------------|----------|
| DDL | Data Definition Language | Commands required to define the database | CREATE, ALTER, DROP, TRUNCATE, RENAME |
| DML | Data Manipulation Language | Commands required to manipulate the data present in the database | SELECT, UPDATE, INSERT, DELETE |
| DCL | Data Control Language | Commands required to deal with user permissions and controls | GRANT, REVOKE |
| TCL | Transaction Control Language | Commands required to deal with the transaction of the database | COMMIT, ROLLBACK, SAVEPOINT |

## 6) ACID properties in DBMS?

ACID stands for **Atomicity**, **Consistency**, **Isolation**, and **Durability** in a DBMS. These are properties that ensure a safe and secure way of sharing data among multiple users.

- **Atomicity**: This property reflects the concept of either executing the whole query or executing nothing at all, which implies that if an update occurs in a database then that update should either be reflected in the whole database or should not be reflected at all.
- **Consistency**: This property ensures that the data remains consistent before and after a transaction in a database.
- **Isolation**: This property ensures that each transaction is occurring independently of the others. This implies that the state of an ongoing transaction doesn't affect the state of another ongoing transaction.
- **Durability**: This property ensures that the data is not lost in cases of a system failure or restart and is present in the same state as it was before the system failure or restart.

## 7) Difference between the DELETE and TRUNCATE command in a DBMS?

| Feature | DELETE Command | TRUNCATE Command |
|---------|---------------|------------------|
| Row removal | Removes rows one by one with transaction logging | Removes all rows at once without transaction logging |
| Rollback | Can be rolled back if required | Can't be rolled back |
| Space | Slower, frees space gradually | Faster, deallocates space immediately |
| Identity | Can reset identity seed | Cannot reset without DBCC command (SQL Server) |

## 8) What is meant by Normalization and Denormalization?

**Normalization** is a process of reducing redundancy by organizing the data into multiple tables. Normalization leads to better usage of disk spaces and makes it easier to maintain the integrity of the database.

**Denormalization** is the reverse process of normalization as it combines the tables which have been normalized into a single table so that data retrieval becomes faster. JOIN operation allows us to create a denormalized form of the data by reversing the normalization.

## 9) Different types of Normalization forms in a DBMS?

### 1NF (First Normal Form)
It is known as the first normal form and is the simplest type of normalization that you can implement in a database. A table to be in its first normal form should satisfy the following conditions:
- Every column must have a single value and should be atomic.
- Duplicate columns from the same table should be removed.
- Separate tables should be created for each group of related data and each row should be identified with a unique column.

### 2NF (Second Normal Form)
It is known as the second normal form. A table to be in its second normal form should satisfy the following conditions:
- The table should be in its 1NF i.e. satisfy all the conditions of 1NF.
- Every non-prime attribute of the table should be fully functionally dependent on the primary key i.e. every non-key attribute should be dependent on the primary key in such a way that if any key element is deleted then even the non_key element will be saved in the database.

### 3NF (Third Normal Form)
It is known as the third normal form. A table to be in its third normal form should satisfy the following conditions:
- The table should be in its 2NF i.e. satisfy all the conditions of 2NF.
- There is no transitive functional dependency of one attribute on any attribute in the same table.

### BCNF (Boyce-Codd Normal Form)
BCNF stands for Boyce-Codd Normal Form and is an advanced form of 3NF. It is also referred to as 3.5NF for the same reason. A table to be in its BCNF normal form should satisfy the following conditions:
- The table should be in its 3NF i.e. satisfy all the conditions of 3NF.
- For every functional dependency of any attribute A on B (A→B), A should be the super key of the table. It simply implies that A can't be a non-prime attribute if B is a prime attribute.

## 10) What is an Entity-Relationship Diagram (ER-Diagram)?

An ER-Diagram is a visual representation of the relationships among entities in a database, showing how different tables are connected.

## 11) Different types of keys in a database?

| Key Type | Description |
|----------|-------------|
| Super Key | A set of one or more attributes that can uniquely identify a record in a table |
| Candidate Key | A minimal set of attributes that can uniquely identify a record, from which the primary key is chosen |
| Primary Key | A candidate key selected to uniquely identify rows, which cannot contain null values or duplicates |
| Alternate Key | A candidate key that is not selected as the primary key |
| Foreign Key | An attribute that establishes a relationship by referencing the primary key of another table |
| Composite Key | A key composed of two or more attributes used together to uniquely identify a record |
| Unique Key | A column constraint ensuring all values are distinct, allowing one null value |
| Surrogate Key | A system-generated, unique identifier usually assigned when no natural key is suitable |
| Compound Key | A type of composite key where each attribute is also a foreign key |
| Secondary Key | An attribute used for indexing and fast data retrieval, not necessarily for unique identification |

## 12) What is a lock? Explain the difference between a shared lock and an exclusive lock?

A database lock is a mechanism to protect a shared piece of data from getting updated by two or more database users at the same time. When a single database user or session has acquired a lock then no other database user or session can modify that data until the lock is released.

| Lock Type | Description |
|-----------|-------------|
| Shared lock | Required for reading a data item. Many transactions may hold a lock on the same data item. When more than one transaction is allowed to read the data items then that is known as the shared lock |
| Exclusive lock | When any transaction is about to perform the write operation, then the lock on the data item is an exclusive lock. Because, if we allow more than one transaction then that will lead to the inconsistency in the database |

## 13) What are Views in DBMS?

A view is a virtual table that is derived from one or more base tables or other views. It does not store any data itself but represents a tailored, pre-defined query that simplifies data retrieval. Views act as a layer of abstraction over the underlying tables, providing a more user-friendly and secure way to interact with the data.

### Benefits of using views:

- **Data Abstraction**: Views allow users to work with a simplified representation of the data, hiding unnecessary details and complexity.
- **Security**: Views can be used to restrict access to certain columns or rows, providing a level of security by only showing specific data to specific users.
- **Simplified Querying**: Complex queries can be encapsulated within views, making it easier for users to retrieve the desired information without writing complex SQL statements.
- **Data Independence**: If the underlying schema changes, views can remain the same, and applications using the views will not be affected.

## 14) What is a Join? List its different types.

The SQL Join clause is used to combine records (rows) from two or more tables in a SQL database based on a related column between the two.

There are four different types of JOINs in SQL:

| Join Type | Description |
|-----------|-------------|
| INNER JOIN | Retrieves records that have matching values in both tables involved in the join. This is the widely used join for queries |
| LEFT OUTER JOIN | Retrieves all the records/rows from the left and the matched records/rows from the right table |
| RIGHT OUTER JOIN | Retrieves all the records/rows from the right and the matched records/rows from the left table |
| FULL OUTER JOIN | Retrieves all the records where there is a match in either the left or right table |

## 15) What is a Self-Join?

A self JOIN is a case of regular join where a table is joined to itself based on some relation between its own column(s). Self-join uses the INNER JOIN or LEFT JOIN clause and a table alias is used to assign different names to the table within the query.

## 16) What is a Cross-Join?

Cross join can be defined as a cartesian product of the two tables included in the join. The table after join contains the same number of rows as in the cross-product of the number of rows in the two tables. If a WHERE clause is used in cross join then the query will work like an INNER JOIN.

## 17) What is an Index? Difference between Clustered and Non-Clustered Index?

A database index is a data structure that provides a quick lookup of data in a column or columns of a table. It enhances the speed of operations accessing data from a database table at the cost of additional writes and memory to maintain the index data structure.

### Difference between Clustered and Non-Clustered Index

| Feature | Clustered Index | Non-Clustered Index |
|---------|----------------|---------------------|
| Storage | Modifies the way records are stored in a database based on the indexed column | Creates a separate entity within the table which references the original table |
| Speed | Used for easy and speedy retrieval of data from the database | Fetching records is relatively slower |
| Quantity per table | Single clustered index per table | Multiple non-clustered indexes per table |
| Key Storage | Physically reorders table data | Stores pointer to data |
| Primary Key | Usually the clustered index | Can be non-clustered |

---

## PostgreSQL vs MySQL Comparison

| Feature | PostgreSQL | MySQL |
|---------|------------|-------|
| Known as | PostgreSQL is an open-source project. The world's most advanced open-source database. | PostgreSQL is an open-source project. |
| Development | PostgreSQL is an open-source project. | MySQL is an open-source product. |
| Pronunciation | post gress queue ell | my ess queue ell |
| Licensing | MIT-style license | GNU General Public License |
| Implementation programming language | C | C/C++ |
| GUI tool | pgAdmin | MySQL Workbench |
| ACID | Yes | Yes |
| Storage engine | Single storage engine | Multiple storage engines e.g., InnoDB and MyISAM |
| Full-text search | Yes | Yes (Limited) |
| Drop a temporary table | No TEMP or TEMPORARY keyword in DROP TABLE statement | Support the TEMP or TEMPORARY keyword in the DROP TABLE statement that allows you to remove the temporary table only. |
| DROP TABLE | Support CASCADE option to drop table's dependent objects e.g., tables and views | Does not support CASCADE option. |
| TRUNCATE TABLE | PostgreSQL TRUNCATE TABLE supports more features like CASCADE, RESTART IDENTITY, CONTINUE IDENTITY, transaction-safe, etc.| MySQL TRUNCATE TABLE does not support CASCADE and transaction safe i.e., once data is deleted, it cannot be rolled back |
| Auto increment Column | SERIAL  | AUTO_INCREMENT |
| Identity Column | Yes | No |
| Window functions | Yes | Yes |
| Data types | Support SQL-standard types as well as user-defined types | SQL-standard types |
| Unsigned integer | No | Yes |
| Boolean type | Yes | Use TINYINT(1) internally for Boolean |
| IP address data type | Yes | No |
| Set a default value for a column | Support both constant and function call | Must be a constant or CURRENT_TIMESTAMP for TIMESTAMP or DATETIME columns |
| CTE | Yes | Yes (Supported CTE since MySQL 8.0) |
| EXPLAIN output | More detailed | Less detailed |
| Materialized views | Yes | No |
| CHECK constraint | Yes | Yes (Supported since MySQL 8.0.16, Before that MySQL just ignored the CHECK constraint) |
| Table inheritance | Yes | No |
| Programming languages for stored procedures | Ruby, Perl, Python, TCL, PL/pgSQL, SQL, JavaScript, etc. | SQL:2003 syntax for stored procedures |
| FULL OUTER JOIN | Yes | No |
| INTERSECT | Yes | Yes (INTERSECT in MySQL 8.0.31) |
| EXCEPT | Yes | Yes |
| Partial indexes | Yes | No |
| Bitmap indexes | Yes | No |
| Expression indexes | Yes | Yes (functional index in MySQL 8.0.13) |
| Covering indexes | Yes (since version 9.2) | Yes. MySQL supports covering indexes that allow data to be retrieved by scanning the index alone without touching the table data. This is advantageous in the case of large tables with millions of rows. |
| Triggers | Support triggers that can fire on most types of command, except for ones affecting the database globally e.g., roles and tablespaces| Limited to some commands |
| Partitioning | RANGE, LIST | RANGE, LIST, HASH, KEY, and composite partitioning using a combination of RANGE or LIST with HASH or KEY subpartitions |
| Task Scheduler | pgAgent | Scheduled event  |
| Connection Scalability | Each new connection is an OS process | Each new connection is an OS thread |
| Replication | Logical (WAL) and physical replication | Binary log replication |
| Async Replication Lag | Generally lower | Generally higher |
| Parallel Query Execution | Yes (since PostgreSQL 9.6) | Limited |
| JSON Support | JSONB with indexing | JSON (limited indexing) |
| Extensions/Plugins | Extensive (PostGIS, pg_trgm, etc.) | Limited |

---

## PostgreSQL-Specific Advanced Features

### 103. JSONB: Efficient JSON Storage and Querying

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  metadata JSONB
);

INSERT INTO users VALUES (1, 'John', '{"location": "NYC", "age": 30, "interests": ["coding", "hiking"]}');

-- Query JSONB data
SELECT * FROM users WHERE metadata->>'location' = 'NYC';
SELECT * FROM users WHERE metadata->'age' > '25'::jsonb;

-- Check if key exists
SELECT * FROM users WHERE metadata ? 'location';

-- Update JSONB
UPDATE users SET metadata = jsonb_set(metadata, '{location}', '"SF"') WHERE id = 1;
```

### 104. PostgreSQL Extensions

```sql
-- Enable PostGIS for geographic queries
CREATE EXTENSION postgis;

-- Enable Text Search
CREATE EXTENSION fts_english;

-- Enable UUID generation
CREATE EXTENSION "uuid-ossp";
SELECT uuid_generate_v4();

-- Enable trigram matching for fuzzy search
CREATE EXTENSION pg_trgm;
CREATE INDEX ON products USING gin (name gin_trgm_ops);
SELECT * FROM products WHERE name % 'iphone';  -- Fuzzy match
```

### 105. Write-Ahead Logging (WAL) and Durability

**Definition**: PostgreSQL writes all changes to a WAL before writing to the actual data files, ensuring durability.

```sql
-- WAL Configuration
-- postgresql.conf
wal_level = replica              # Minimum for replication
max_wal_senders = 3              # Number of replication connections
wal_keep_size = 1GB              # Keep WAL files for standby
synchronous_commit = on          # Wait for WAL flush before ACK
```

**WAL Archiving:**
```sql
-- postgresql.conf
archive_mode = on
archive_command = 'cp %p /mnt/wal_archive/%f'
```

### 106. VACUUM and Table Maintenance

```sql
-- Manual VACUUM (removes dead rows)
VACUUM employees;

-- VACUUM ANALYZE (also updates statistics)
VACUUM ANALYZE employees;

-- Full VACUUM (locks table, slower but thorough)
VACUUM FULL employees;

-- Autovacuum (runs automatically)
-- ALTER SYSTEM SET autovacuum = on;
```

### 107. Partitioning Strategies in PostgreSQL

**Range Partitioning:**
```sql
CREATE TABLE events (
  id INT,
  event_date DATE,
  data TEXT
) PARTITION BY RANGE (event_date);

CREATE TABLE events_2023_q1 PARTITION OF events
  FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');
CREATE TABLE events_2023_q2 PARTITION OF events
  FOR VALUES FROM ('2023-04-01') TO ('2023-07-01');
```

**List Partitioning:**
```sql
CREATE TABLE sales (
  id INT,
  region VARCHAR(50),
  amount DECIMAL
) PARTITION BY LIST (region);

CREATE TABLE sales_us PARTITION OF sales
  FOR VALUES IN ('California', 'Texas', 'New York');
CREATE TABLE sales_eu PARTITION OF sales
  FOR VALUES IN ('UK', 'Germany', 'France');
```

**Hash Partitioning:**
```sql
CREATE TABLE logs (
  id BIGSERIAL,
  message TEXT
) PARTITION BY HASH (id);

CREATE TABLE logs_0 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE logs_1 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 1);
```

---

## Performance Tuning Checklist

1. **Monitor Slow Queries**
   - Enable slow query log
   - Use `log_min_duration_statement = 1000` (log queries > 1 second)
   - Analyze with `EXPLAIN ANALYZE`

2. **Index Strategy**
   - Create indexes on frequently filtered/joined columns
   - Use partial indexes for common WHERE conditions
   - Remove unused indexes (check pg_stat_user_indexes)

3. **Statistics**
   - Run `ANALYZE` regularly
   - Check `default_statistics_target` (higher = more accurate)

4. **Connection Management**
   - Use connection pooling (PgBouncer, pgpool)
   - Monitor `pg_stat_activity` for long-running queries
   - Set appropriate `statement_timeout`

5. **Memory Configuration**
   - `shared_buffers`: 25% of RAM (caching)
   - `effective_cache_size`: 50-75% of RAM
   - `work_mem`: RAM / (max_connections * 2)

6. **Replication & Backup**
   - Enable WAL archiving for Point-in-Time Recovery
   - Use `pg_basebackup` for full backups
   - Monitor replication lag

7. **Maintenance**
   - Schedule regular `VACUUM ANALYZE`
   - Monitor table bloat
   - REINDEX bloated indexes

---

## Additional Resources

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL Performance Tuning Guide](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [EXPLAIN Query Plans](https://www.postgresql.org/docs/current/sql-explain.html)
- [Transaction Isolation Levels](https://www.postgresql.org/docs/current/transaction-iso.html)
- [Further SQL and DBMS Concepts](https://leetcode.com/discuss/post/3823497/dbms-cheatsheet-for-interviews-30-questi-wnci/)

---

**Last Updated**: 2025 | Created for Senior Engineers
