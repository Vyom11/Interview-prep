# 🔐 FastAPI Security: Authentication & Authorization Guide

> A comprehensive, production-oriented guide for securing FastAPI applications.
> Written for junior developers, detailed enough for a production overview.

-----

## 📖 Table of Contents

1. [Core Concepts: JWT vs. Session vs. OAuth2](#1-core-concepts-jwt-vs-session-vs-oauth2)
1. [Practical Code Example](#2-practical-code-example)
1. [Real-World Scenario: The E-Commerce Hub](#3-real-world-scenario-the-e-commerce-hub)
1. [Security Feature Checklist](#4-security-feature-checklist)

-----

## 1. Core Concepts: JWT vs. Session vs. OAuth2

Before diving into code, it’s important to understand *what* each mechanism does and *why* it exists.

-----

### 🎟️ JWT — JSON Web Token

#### Simple Definition

Think of a JWT like a **concert wristband**. Once you’ve shown your ID at the door (logged in), the venue gives you a wristband. For the rest of the night, staff just glance at your wrist — they don’t need to check your ID every time. The wristband itself contains enough information to verify who you are.

> **Key point:** JWTs are **stateless** — the server doesn’t need to remember you. All the information lives *inside* the token.

#### The Workflow

```
1. Client  →  POST /login  (username + password)
2. Server  →  Validates credentials against the database
3. Server  →  Creates a JWT: { "sub": "user123", "exp": 1700000000 }
4. Server  →  Signs the token with a SECRET_KEY and sends it back
5. Client  →  Stores the token (usually in memory or localStorage)
6. Client  →  On every protected request: sends token in the Authorization header
               "Authorization: Bearer <token>"
7. Server  →  Decodes and verifies the signature — NO database lookup needed
8. Server  →  Grants or denies access
```

#### FastAPI Implementation

|Tool                  |Purpose                                                                                          |
|----------------------|-------------------------------------------------------------------------------------------------|
|`python-jose`         |Encodes and decodes JWT tokens (`jwt.encode`, `jwt.decode`)                                      |
|`OAuth2PasswordBearer`|A FastAPI utility that tells the framework *where* to find the token (the `Authorization` header)|
|`HTTPBearer`          |A lower-level security scheme for extracting Bearer tokens from requests                         |

```python
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
```

-----

### 🍪 Session — Server-Side Sessions

#### Simple Definition

Think of sessions like a **coat check at a restaurant**. You hand over your coat (credentials), and they give you a small ticket (a session ID cookie). They store your coat on their side. Every time you show the ticket, they look up your coat in their storage room.

> **Key point:** Sessions are **stateful** — the server *does* remember you. Your data lives on the server; the client only holds a reference ID.

#### The Workflow

```
1. Client  →  POST /login  (username + password)
2. Server  →  Validates credentials
3. Server  →  Creates a session record in the database/Redis: { session_id: "abc123", user_id: 42 }
4. Server  →  Sends back a Set-Cookie header: "session_id=abc123"
5. Client  →  Browser automatically stores and sends the cookie on every request
6. Server  →  Receives "session_id=abc123", looks it up in the session store
7. Server  →  Retrieves user data and grants access
```

#### FastAPI Implementation

|Tool               |Purpose                                                  |
|-------------------|---------------------------------------------------------|
|`itsdangerous`     |Signs session cookies to prevent tampering               |
|`starlette-session`|Middleware that adds `request.session` support to FastAPI|
|`Redis` / database |Backend store for session data                           |

```python
from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(SessionMiddleware, secret_key="your-secret")
# Now use request.session["user_id"] = 42 in your routes
```

-----

### 🌐 OAuth2 — Open Authorization 2.0

#### Simple Definition

OAuth2 is like a **valet parking service**. You hand the valet a *special limited key* (an access token) that only opens the car door — not your house, your mailbox, or your safe. A third party gets *limited, specific access* to your resources without ever seeing your real password.

> **Key point:** OAuth2 is an **authorization framework**, not just an authentication method. It enables one application to act on behalf of a user within another application.

#### The Workflow (Authorization Code Flow)

```
1. User     →  Clicks "Login with Google" on your app
2. Your App →  Redirects user to Google's Authorization Server
               (with your client_id, requested scopes, redirect_uri)
3. User     →  Logs into Google and clicks "Allow"
4. Google   →  Redirects back to your app with a short-lived `code`
5. Your App →  Exchanges the `code` + `client_secret` for an `access_token`
               (this exchange happens server-to-server, never in the browser)
6. Your App →  Uses the `access_token` to call Google APIs on behalf of the user
7. Google   →  Returns the requested data (e.g., user's email, profile)
```

#### FastAPI Implementation

|Tool                           |Purpose                                                                                            |
|-------------------------------|---------------------------------------------------------------------------------------------------|
|`OAuth2PasswordBearer`         |FastAPI’s built-in helper for the Resource Owner Password flow (simpler, used for first-party apps)|
|`OAuth2AuthorizationCodeBearer`|For the full Authorization Code flow (third-party “Login with X”)                                  |
|`Authlib` / `httpx-oauth`      |Popular libraries for handling the full OAuth2 client flow                                         |

```python
from fastapi.security import OAuth2AuthorizationCodeBearer

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token"
)
```

-----

## 2. Practical Code Example

A single, focused script demonstrating password hashing, JWT creation, and a protected route.

### Prerequisites

```bash
pip install fastapi "python-jose[cryptography]" "passlib[bcrypt]" uvicorn
```

### `security_example.py`

```python
# ─── Imports ──────────────────────────────────────────────────────────────────

from datetime import datetime, timedelta       # Used to set token expiry time
from typing import Optional                    # For optional type hints

from fastapi import FastAPI, Depends, HTTPException, status  # Core FastAPI pieces
from fastapi.security import OAuth2PasswordBearer            # Extracts Bearer token from headers
from jose import JWTError, jwt                               # Encodes/decodes JWT tokens
from passlib.context import CryptContext                     # Manages password hashing

# ─── Configuration ────────────────────────────────────────────────────────────

# The secret key used to SIGN the JWT — keep this private and never commit it to git
SECRET_KEY = "your-super-secret-key-replace-in-production"

# The algorithm used to sign the token — HS256 is a standard symmetric algorithm
ALGORITHM = "HS256"

# How long (in minutes) before a token expires and the user must log in again
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ─── Password Hashing Setup ───────────────────────────────────────────────────

# Create a hashing context using bcrypt — bcrypt is slow by design, resisting brute-force
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ─── Fake Database ────────────────────────────────────────────────────────────

# In production, this would be a real database (PostgreSQL, etc.)
# The password stored here is the HASH of "secret123", NOT the plain-text password
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": pwd_context.hash("secret123"),  # Hash generated at registration time
    }
}

# ─── FastAPI App & Security Scheme ────────────────────────────────────────────

app = FastAPI()

# Tells FastAPI: "tokens will arrive as Bearer tokens, and users can get them at /token"
# This also auto-generates an Authorize button in the /docs UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ─── Helper: Verify Password ──────────────────────────────────────────────────

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Compares a raw plain-text password against a stored hash — returns True/False
    # passlib handles the bcrypt comparison internally (including the salt)
    return pwd_context.verify(plain_password, hashed_password)

# ─── Helper: Create JWT Token ─────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # Copy the payload so we don't mutate the original dictionary
    to_encode = data.copy()

    # Calculate when the token should expire
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))

    # Add the expiry timestamp to the token payload under the key "exp"
    # The jose library will automatically validate this field on decode
    to_encode.update({"exp": expire})

    # Encode the payload into a signed JWT string using our SECRET_KEY
    # The result is a compact string like: "xxxxx.yyyyy.zzzzz"
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt  # Return the finished token string

# ─── Route: Login & Get Token ─────────────────────────────────────────────────

@app.post("/token")
def login(username: str, password: str):
    # Look up the user in our fake database by username
    user = fake_users_db.get(username)

    # If the user doesn't exist, or their password doesn't match — reject immediately
    if not user or not verify_password(password, user["hashed_password"]):
        # 401 Unauthorized — credentials are wrong
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},  # Tells client what auth scheme to use
        )

    # Set the token to expire after our configured duration
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Create the JWT token — "sub" (subject) is a standard JWT claim for user identity
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=token_expires
    )

    # Return the token and its type — clients should send this as "Bearer <access_token>"
    return {"access_token": access_token, "token_type": "bearer"}

# ─── Helper: Decode & Validate Token ─────────────────────────────────────────

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    # If credentials cannot be validated, this error will be raised
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT — jose automatically checks the signature and expiry time
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the username from the "sub" (subject) claim
        username: str = payload.get("sub")

        # If "sub" is missing from the token, it's malformed — reject it
        if username is None:
            raise credentials_exception

    except JWTError:
        # JWTError is raised if the token is expired, tampered with, or malformed
        raise credentials_exception

    # Confirm this user still exists in our database
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception  # Token was valid, but the user no longer exists

    return username  # Return the verified username to the calling route

# ─── Protected Route ──────────────────────────────────────────────────────────

@app.get("/profile")
def read_profile(current_user: str = Depends(get_current_user)):
    # `Depends(get_current_user)` runs get_current_user() BEFORE this function executes
    # If the token is invalid, get_current_user() raises an HTTPException and this never runs
    # If the token is valid, `current_user` contains the verified username
    return {"message": f"Hello, {current_user}! This is your protected profile."}
```

### How to Run & Test

```bash
# Start the server
uvicorn security_example:app --reload

# 1. Get a token (replace with your credentials)
curl -X POST "http://127.0.0.1:8000/token?username=johndoe&password=secret123"

# 2. Use the token to access the protected route
curl -H "Authorization: Bearer <paste_token_here>" http://127.0.0.1:8000/profile

# Or visit http://127.0.0.1:8000/docs for the interactive Swagger UI
```

-----

## 3. Real-World Scenario: The E-Commerce Hub

Imagine a marketplace like Amazon or a specialized ML model marketplace. Here’s where each security mechanism earns its place.

-----

### 🛒 Where Would You Use Sessions?

**Use Case: Guest Shopping Carts**

When a visitor browses your marketplace *without logging in*, you still want to track their cart. A server-side session is perfect here:

- The server creates a session record the moment they add their first item
- A session cookie is sent to the browser silently
- If they close the tab and return within the session window, their cart is still there
- Sessions are also ideal for **multi-step checkout flows**, where you need to preserve state (shipping → payment → confirmation) without exposing data in the URL or a client-side token

> ✅ **Best for:** Temporary, anonymous state. High-trust internal flows. Traditional server-rendered pages.

-----

### 🔑 Where Would You Use JWT?

**Use Case: Accessing a User’s Private Order History via API**

Once a user logs in through your mobile app or SPA (Single Page App), you issue them a JWT. Now they can:

- Fetch their order history: `GET /api/orders` with `Authorization: Bearer <token>`
- Access their saved addresses, payment methods, and preferences
- Interact with a **microservices backend** — the JWT can be forwarded from your Orders service to your Shipping service without any shared session store between them

Because JWTs are **self-contained**, they work seamlessly across services that don’t share a database. This is especially powerful in distributed architectures.

> ✅ **Best for:** API-first applications, mobile apps, SPAs, microservices communication.

-----

### 🌐 Where Would You Use OAuth2?

**Use Case 1: “Login with Google”**

Instead of managing passwords yourself, you delegate authentication to Google:

- The user clicks “Login with Google”
- Google authenticates them and returns a token confirming their identity
- Your app uses that token to create or log in a local account
- You never see their Google password

**Use Case 2: Third-Party Shipping Tracker**

A user wants to connect a third-party app (e.g., a shipping dashboard) to track their orders:

- Your marketplace becomes the **Resource Server**
- The third-party app requests a scoped token: `scope: "read:orders"`
- The user approves — the app can now read their orders but *cannot* change their password, view payment info, or do anything outside its granted scope

> ✅ **Best for:** Social login (“Login with X”), delegating limited access to third-party apps, enterprise SSO.

-----
## Real-World Example: An E-commerce Website (e.g., Amazon)
Let's look at how all three live together on a single platform:

* OAuth2 (The "Login with Google" button): When you click "Login with Google" on the store, you are redirected to Google. Google gives the store an Access Token to see your name and email. The store never sees your Google password.
* Sessions (The "Guest Shopping Cart"): If you are browsing items without logging in, the site might use a Session to remember what's in your cart. A temporary cookie is stored in your browser so if you refresh the page, your items don't disappear.
* JWT (The "User Profile & Checkout"): Once you log in, the store's API sends your browser a JWT. When you click "View My Orders" or "Checkout," your browser sends that JWT to the backend. Because the JWT is stateless, the backend can quickly verify you are "User #456" without hitting the database to check a session table every single time. [1, 2] 

## 4. Security Feature Checklist

Use this as a reference when auditing or building your FastAPI security layer.

-----

### 🪪 Authentication vs. Authorization

These two terms are often confused. They solve *different* problems.

|Concept           |Question It Answers          |Analogy                                          |
|------------------|-----------------------------|-------------------------------------------------|
|**Authentication**|*Who are you?*               |Showing your **ID card** at the door             |
|**Authorization** |*What are you allowed to do?*|Using a **keycard** that only opens certain rooms|


> **Example:** A user might successfully *authenticate* (prove they are `johndoe`), but when they try to access `/admin`, **authorization** checks fail because `johndoe` does not have the `admin` role.

In FastAPI, this maps to:

```python
# Authentication — verifying identity via JWT
current_user = Depends(get_current_user)

# Authorization — checking what the verified user can do
if current_user.role != "admin":
    raise HTTPException(status_code=403, detail="Forbidden")
```

-----

### 🔒 Bcrypt: Why We Never Store Plain-Text Passwords

Storing a plain-text password is one of the most dangerous mistakes in web development. If your database is ever compromised, every user’s password is immediately exposed.

**What Bcrypt does:**

1. Takes a plain-text password (e.g., `"secret123"`)
1. Adds a **random salt** (a random string appended to prevent identical passwords from producing identical hashes)
1. Runs an intentionally **slow hashing algorithm** (making brute-force attacks impractical)
1. Produces a fixed-length hash (e.g., `$2b$12$...`)

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# At registration — store only the hash, NEVER the plain-text password
hashed = pwd_context.hash("secret123")

# At login — compare plain-text input against the stored hash
is_valid = pwd_context.verify("secret123", hashed)  # Returns True
```

> ✅ **Rule:** A database breach should expose *only* bcrypt hashes. Even if attackers get the database, cracking bcrypt hashes for a large user base is computationally infeasible.

-----

### 🗝️ API Keys: When to Use a Simple Header Key

JWTs are powerful, but they carry overhead. For certain use cases, a simple **API Key** in a request header is the right tool.

**When to use API Keys instead of JWT:**

|Scenario                     |Why API Keys Fit                          |
|-----------------------------|------------------------------------------|
|Internal ML model endpoints  |Machine-to-machine, no human user involved|
|Batch processing services    |One service calling another service       |
|Simple read-only integrations|Low-risk, no user context needed          |
|Developer/partner API access |Long-lived keys, easy to revoke           |

```python
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

# Define that we expect the key in a header called "X-API-Key"
api_key_header = APIKeyHeader(name="X-API-Key")

# Our valid keys — in production, store these in environment variables or a secrets manager
VALID_API_KEYS = {"ml-service-key-abc123", "partner-key-xyz789"}

def verify_api_key(api_key: str = Security(api_key_header)):
    # Check if the provided key exists in our set of valid keys
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key  # Key is valid, proceed

@app.get("/ml/predict")
def run_prediction(api_key: str = Depends(verify_api_key)):
    # Only reachable if a valid X-API-Key header was provided
    return {"prediction": "model output here"}
```

> ✅ **Rule of thumb:** Use **API Keys** for service-to-service or developer access where there’s no interactive user. Use **JWT** when you need to carry user identity and claims between requests.

-----

## Summary: Choosing the Right Tool

|Mechanism  |Best For                                         |Stateful?                     |User-Facing?             |
|-----------|-------------------------------------------------|------------------------------|-------------------------|
|**Session**|Server-rendered apps, guest carts, checkout flows|✅ Yes (server stores state)   |✅ Yes                    |
|**JWT**    |APIs, mobile apps, microservices, SPAs           |❌ No (token is self-contained)|✅ Yes                    |
|**OAuth2** |Social login, third-party delegation, SSO        |Depends on flow               |✅ Yes                    |
|**API Key**|Internal services, ML endpoints, partner APIs    |❌ No                          |❌ No (machine-to-machine)|

-----

## 📚 Further Reading

- [FastAPI Security Docs](https://fastapi.tiangolo.com/tutorial/security/)
- [python-jose Documentation](https://python-jose.readthedocs.io/en/latest/)
- [passlib Documentation](https://passlib.readthedocs.io/en/stable/)
- [OAuth2 Simplified (aaronparecki.com)](https://aaronparecki.com/oauth-2-simplified/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

-----

*Last updated: 2026 · Built for FastAPI 0.100+ · Python 3.10+*
