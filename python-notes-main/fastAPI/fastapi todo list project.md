# ✅ FastAPI To-Do App

A simple To-Do API where users can sign up, log in, and manage their own tasks. Built with FastAPI, PostgreSQL, and JWT tokens.

-----

## 📋 Table of Contents

1. [What This App Does](#what-this-app-does)
1. [Tools Used](#tools-used)
1. [Project Structure](#project-structure)
1. [Setup](#setup)
1. [Database Tables](#database-tables)
1. [How Login Works](#how-login-works)
1. [Task Operations](#task-operations)
1. [Error Responses](#error-responses)
1. [API Endpoints](#api-endpoints)
1. [Running the App](#running-the-app)
1. [Testing Your API](#testing-your-api)
1. [Running Tests](#running-tests)
1. [Going Live](#going-live)

-----

## What This App Does

Users can:

- Create an account and log in
- Add, view, edit, and delete their own tasks
- Only see their own tasks — never anyone else’s

-----

## Tools Used

|Tool          |What it does                                                  |
|--------------|--------------------------------------------------------------|
|**FastAPI**   |Builds the API and handles incoming requests                  |
|**PostgreSQL**|Stores users and tasks in a database                          |
|**SQLAlchemy**|Lets us work with the database using Python instead of raw SQL|
|**Alembic**   |Updates the database when we change our models                |
|**JWT**       |A token given to users after login so they stay logged in     |
|**Bcrypt**    |Scrambles passwords so they’re safe to store                  |
|**Pydantic**  |Checks that the data sent to the API is valid                 |
|**pytest**    |Runs automated tests to make sure everything works            |

### How a Request Travels Through the App

```
User sends a request
       │
       ▼
FastAPI checks the data is valid
       │
       ▼
Check: is the user logged in? (read their JWT token)
       │
       ▼
Run the task (create, read, update, delete)
       │
       ▼
Talk to the database
       │
       ▼
Send a response back to the user
```

-----

## Project Structure

```
fastapi-todo/
│
├── app/
│   ├── main.py            # Starts the app, connects all the routes
│   ├── config.py          # Reads settings from the .env file
│   ├── database.py        # Connects to PostgreSQL
│   │
│   ├── models/
│   │   ├── user.py        # What a User looks like in the database
│   │   └── task.py        # What a Task looks like in the database
│   │
│   ├── schemas/
│   │   ├── user.py        # What data is needed to create/return a User
│   │   └── task.py        # What data is needed to create/return a Task
│   │
│   ├── routers/
│   │   ├── auth.py        # /register and /login routes
│   │   └── tasks.py       # Routes for managing tasks
│   │
│   ├── services/
│   │   ├── auth_service.py   # Handles tokens and passwords
│   │   └── task_service.py   # Handles task logic
│   │
│   └── dependencies.py    # Shared helpers (open DB, check who's logged in)
│
├── tests/
│   ├── conftest.py        # Test setup (fake database, test user)
│   ├── test_auth.py       # Tests for register and login
│   └── test_tasks.py      # Tests for task operations
│
├── alembic/               # Database migration files
├── requirements.txt
├── .env.example
└── README.md
```

-----

## Setup

### Step 1 — Download the project

```bash
git clone https://github.com/your-username/fastapi-todo.git
cd fastapi-todo

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### Step 2 — Install packages

```bash
pip install -r requirements.txt
```

**`requirements.txt`**

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.30
alembic==1.13.1
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.1
pydantic-settings==2.2.1
pytest==8.2.0
httpx==0.27.0
```

### Step 3 — Add your settings

Copy the example file and fill in your details:

```bash
cp .env.example .env
```

**`.env`**

```env
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db

SECRET_KEY=change-this-to-a-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Tip:** Make a strong `SECRET_KEY` by running: `openssl rand -hex 32`

### Step 4 — Create the database

```bash
psql -U postgres
CREATE DATABASE todo_db;
\q
```

### Step 5 — Set up the tables

```bash
alembic upgrade head
```

-----

## Database Tables

Each user can have many tasks. The `owner_id` column in the tasks table links each task back to the user who created it.

```
┌─────────────┐          ┌──────────────────┐
│    users    │          │      tasks       │
├─────────────┤          ├──────────────────┤
│ id          │◄────────┤ owner_id         │
│ email       │          │ id               │
│ username    │          │ title            │
│ password    │          │ description      │
│ is_active   │          │ is_completed     │
│ created_at  │          │ created_at       │
└─────────────┘          └──────────────────┘
```

### User table

```
User has:
  - id          → a unique number for each user
  - email       → must be unique, used to identify the user
  - username    → must be unique
  - password    → stored scrambled (hashed), never plain text
  - is_active   → True by default, can be disabled
  - created_at  → automatically set when the user signs up
  - tasks       → list of all tasks belonging to this user
                  (if user is deleted, their tasks are deleted too)
```

### Task table

```
Task has:
  - id           → a unique number for each task
  - title        → short name for the task (required)
  - description  → longer notes (optional)
  - is_completed → False by default, set to True when done
  - created_at   → set automatically
  - updated_at   → updates automatically when task is edited
  - owner_id     → links to the user who created this task
```

-----

## How Login Works

### Signing Up

```
1. User sends their email, username, and password
2. App checks: is this email already taken? → reject if yes
3. App scrambles (hashes) the password with Bcrypt
4. App saves the new user to the database
5. App returns the user's info (no password included)
```

### Logging In

```
1. User sends their username and password
2. App looks up the user by username → reject if not found
3. App checks: does the password match the stored hash? → reject if not
4. App creates a JWT token:
     - Contains: user's ID and an expiry time (30 minutes)
     - Signed with the SECRET_KEY so it can't be faked
5. App returns the token to the user
```

### Making a Logged-In Request

```
1. User includes the token in the request header:
     Authorization: Bearer <token>
2. App reads and checks the token:
     - Is it expired?          → reject
     - Has it been tampered?   → reject
     - Does the user exist?    → reject if not
3. App continues with the request using the user's info
```

### Token helper functions

```
hash_password(password):
    → scramble the password and return the hashed version

check_password(plain, hashed):
    → return True if they match, False if not

create_token(user_id):
    → build a token with the user_id and expiry time
    → sign it and return it as a string

read_token(token):
    → decode the token
    → if expired  → send a 401 error
    → if invalid  → send a 401 error
    → if valid    → return the data inside
```

-----

## Task Operations

Every task operation first checks: **does this task belong to the logged-in user?**

```
check_owner(task_id, current_user):
    task = find task by id
    if not found        → send 404 error
    if wrong owner      → send 403 error
    return task
```

### Create a task

```
create_task(title, description, current_user):
    make a new task:
        title       = what the user sent
        description = what the user sent
        owner_id    = current_user's id
    save to database
    return the new task
```

### Get all tasks

```
get_my_tasks(current_user):
    fetch tasks WHERE owner_id = current_user.id
    sort by newest first
    return the list
```

### Update a task

```
update_task(task_id, new_data, current_user):
    run check_owner → stop here if not allowed
    update the fields that were sent
    save changes
    return the updated task
```

### Delete a task

```
delete_task(task_id, current_user):
    run check_owner → stop here if not allowed
    delete the task
    return nothing (204 No Content)
```

-----

## Error Responses

Every error returns JSON in this shape:

```json
{
  "error": "Not Found",
  "detail": "Task with id 5 does not exist."
}
```

### Status codes used

|Code |Meaning      |Example                           |
|-----|-------------|----------------------------------|
|`200`|OK           |Task fetched                      |
|`201`|Created      |New task or user created          |
|`204`|Deleted      |Task deleted, nothing returned    |
|`400`|Bad request  |Email already in use              |
|`401`|Not logged in|Token missing or expired          |
|`403`|Not allowed  |Trying to edit someone else’s task|
|`404`|Not found    |Task ID doesn’t exist             |
|`422`|Invalid data |Missing a required field          |
|`500`|Server error |Something unexpected broke        |


> **Note:** For wrong username or wrong password, the app returns the same `401` message either way. This stops attackers from figuring out which usernames exist.

-----

## API Endpoints

### Auth

|Method|URL                    |Login needed|What it does          |
|------|-----------------------|------------|----------------------|
|`POST`|`/api/v1/auth/register`|No          |Create a new account  |
|`POST`|`/api/v1/auth/login`   |No          |Log in and get a token|

### Tasks

|Method  |URL                 |Login needed|What it does      |
|--------|--------------------|------------|------------------|
|`GET`   |`/api/v1/tasks/`    |Yes         |Get all your tasks|
|`POST`  |`/api/v1/tasks/`    |Yes         |Create a new task |
|`GET`   |`/api/v1/tasks/{id}`|Yes         |Get one task      |
|`PUT`   |`/api/v1/tasks/{id}`|Yes         |Update a task     |
|`DELETE`|`/api/v1/tasks/{id}`|Yes         |Delete a task     |

### Example: Login

Request:

```json
{
  "username": "johndoe",
  "password": "mypassword123"
}
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Example: Create a task

Include the header: `Authorization: Bearer <your_token>`

Request:

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

Response:

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "created_at": "2025-04-20T14:32:00Z",
  "owner_id": 7
}
```

-----

## Running the App

```bash
# Development — restarts automatically when you change code
uvicorn app.main:app --reload

# Production — handles more traffic with 4 workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

-----

## Testing Your API

FastAPI builds a test page for you automatically — no extra setup needed.

|Page          |URL                          |Use it to                    |
|--------------|-----------------------------|-----------------------------|
|**Swagger UI**|`http://localhost:8000/docs` |Click and test endpoints live|
|**ReDoc**     |`http://localhost:8000/redoc`|Read clean documentation     |

### How to test a protected endpoint in Swagger UI

1. Open `http://localhost:8000/docs`
1. Call `POST /api/v1/auth/login` and copy the `access_token` from the response
1. Click the **Authorize** button 🔒 at the top
1. Paste: `Bearer <your_token>`
1. All requests will now include the token automatically

-----

## Running Tests

Tests use a temporary in-memory database — they never touch your real data.

### The 5 tests

**`tests/test_auth.py`**

```python
# Test 1: Register a new user — should return 201
def test_register_success(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "Pass123!"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert "password" not in response.json()  # password must never be returned


# Test 2: Register with the same email twice — should return 400
def test_register_duplicate_email(client):
    data = {"email": "same@example.com", "username": "user1", "password": "Pass123!"}
    client.post("/api/v1/auth/register", json=data)

    data["username"] = "user2"  # same email, different username
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 400


# Test 3: Log in with correct details — should return a token
def test_login_success(client):
    client.post("/api/v1/auth/register", json={
        "email": "login@example.com",
        "username": "loginuser",
        "password": "Pass123!"
    })
    response = client.post("/api/v1/auth/login", data={
        "username": "loginuser",
        "password": "Pass123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

**`tests/test_tasks.py`**

```python
# Test 4: Logged-in user can create and then fetch a task
def test_create_and_get_task(client, auth_headers):
    # Create the task
    create = client.post("/api/v1/tasks/",
                         json={"title": "My Task", "description": "Details"},
                         headers=auth_headers)
    assert create.status_code == 201
    task_id = create.json()["id"]

    # Fetch the task
    get = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert get.status_code == 200
    assert get.json()["title"] == "My Task"


# Test 5: One user cannot read another user's task — should return 403
def test_cannot_read_other_users_task(client):
    # User A signs up and creates a task
    client.post("/api/v1/auth/register", json={
        "email": "a@example.com", "username": "user_a", "password": "Pass123!"
    })
    login_a = client.post("/api/v1/auth/login",
                          data={"username": "user_a", "password": "Pass123!"})
    token_a = {"Authorization": f"Bearer {login_a.json()['access_token']}"}

    task = client.post("/api/v1/tasks/",
                       json={"title": "User A's task"},
                       headers=token_a)
    task_id = task.json()["id"]

    # User B signs up and tries to read User A's task
    client.post("/api/v1/auth/register", json={
        "email": "b@example.com", "username": "user_b", "password": "Pass123!"
    })
    login_b = client.post("/api/v1/auth/login",
                          data={"username": "user_b", "password": "Pass123!"})
    token_b = {"Authorization": f"Bearer {login_b.json()['access_token']}"}

    response = client.get(f"/api/v1/tasks/{task_id}", headers=token_b)
    assert response.status_code == 403  # blocked — not their task
```

### Run the tests

```bash
# Run all tests
pytest tests/ -v

# See which lines of code are covered
pytest tests/ -v --cov=app --cov-report=term-missing
```

Expected result:

```
tests/test_auth.py::test_register_success              PASSED
tests/test_auth.py::test_register_duplicate_email      PASSED
tests/test_auth.py::test_login_success                 PASSED
tests/test_tasks.py::test_create_and_get_task          PASSED
tests/test_tasks.py::test_cannot_read_other_users_task PASSED

5 passed in 1.43s
```

-----

## Going Live

### Step 1 — Docker

Package the app and database together with Docker, then start everything with:

```bash
docker-compose up
```

### Step 2 — Security checklist before deploying

- Change `SECRET_KEY` to a long random value
- Turn off debug mode
- Hide the `/docs` page in production
- Never hardcode passwords — use environment variables
- Only allow your frontend’s domain in CORS settings

### Step 3 — Run migrations before each deploy

```bash
alembic upgrade head
```

### Step 4 — Cloud options

|Platform            |How to deploy                                          |
|--------------------|-------------------------------------------------------|
|**AWS**             |ECS + RDS PostgreSQL                                   |
|**GCP**             |Cloud Run + Cloud SQL                                  |
|**Heroku**          |Add `web: uvicorn app.main:app` to a Procfile          |
|**Railway / Render**|Connect your GitHub repo, set env vars in the dashboard|

### Step 5 — Add logging

Once live, add basic logging so you can see what’s happening:

- Use Python’s built-in `logging` module to record errors
- Add a `/health` endpoint that returns `200 OK`
- Use a tool like Sentry to get notified when something breaks

-----

## Contributing

Open an issue before making big changes. Make sure all 5 tests pass before submitting a pull request.

-----

## License

MIT License. See `LICENSE` for details.
