# Professional Notes App Backend (FastAPI)

# Goal

Build a production-style multi-user Notes Backend API using:

* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT Authentication
* Alembic
* Docker
* Render Deployment

This project should look like a real backend engineering assignment submission.

---



### Authentication

* User Registration
* User Login
* JWT Authentication

### Notes

* Create Notes
* Read Notes
* Update Notes
* Delete Notes
* Share Notes

### API Docs

* /openapi.json
* /docs

### About Endpoint

* /about

---



# Note Version History + Restore


Real user problem:
Users accidentally overwrite important notes.

Solution:
Every time a note is updated:

* previous version gets saved
* user can restore older versions

This demonstrates:

* Product thinking
* Backend architecture
* Data modeling
* Audit/history systems
* Non-trivial implementation


---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Pydantic
* Alembic

## Authentication

* JWT
* bcrypt password hashing

## Deployment

* Render

## Optional

* Docker

---

# Project Structure

```txt
notes-app/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   ├── config.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── notes.py
│   │   ├── history.py
│   │   └── about.py
│   │
│   └── services/
│       ├── note_service.py
│       └── share_service.py
│
├── alembic/
├── requirements.txt
├── Dockerfile
├── .env
├── README.md
└── .gitignore
```

---

# Step 1 — Setup Environment

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

# Step 2 — Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib[bcrypt] python-dotenv alembic pydantic[email]
```

---

# Step 3 — requirements.txt

```txt
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-jose
passlib[bcrypt]
python-dotenv
alembic
pydantic[email]
```

---

# Step 4 — Database Design

# users Table

```sql
id UUID PRIMARY KEY
email VARCHAR UNIQUE NOT NULL
password_hash VARCHAR NOT NULL
created_at TIMESTAMP
```

---

# notes Table

```sql
id UUID PRIMARY KEY
owner_id UUID REFERENCES users(id)
title VARCHAR NOT NULL
content TEXT
created_at TIMESTAMP
updated_at TIMESTAMP
```

---

# note_shares Table

```sql
id UUID PRIMARY KEY
note_id UUID REFERENCES notes(id)
shared_with_id UUID REFERENCES users(id)
created_at TIMESTAMP
```

---

# note_versions Table 

```sql
id UUID PRIMARY KEY
note_id UUID REFERENCES notes(id)
title VARCHAR
content TEXT
version_number INTEGER
created_at TIMESTAMP
```

---

# Step 5 — Authentication Flow

# Register

```txt
POST /register
```

## Tasks

* Validate email
* Hash password
* Save user

---

# Login

```txt
POST /login
```

## Tasks

* Verify password
* Generate JWT token

Example Response:

```json
{
  "access_token": "jwt_token"
}
```

---

# JWT Payload

```python
{
    "sub": user.email,
    "user_id": str(user.id)
}
```

---

# Step 6 — Protected Routes

Protected routes require:

```txt
Authorization: Bearer <token>
```

Use reusable dependency:

```python
get_current_user()
```

---

# Step 7 — Notes APIs

# Create Note

```txt
POST /notes
```

Payload:

```json
{
  "title": "Shopping",
  "content": "Milk"
}
```

---

# Get All Notes

```txt
GET /notes
```

Return:

* owned notes
* optionally shared notes

---

# Get Single Note

```txt
GET /notes/{id}
```

Rules:

* owner can access
* shared users can access
* others cannot

---

# Update Note

```txt
PUT /notes/{id}
```

Before updating:

* save previous version into note_versions


---

# Delete Note

```txt
DELETE /notes/{id}
```

Only owner allowed.

---

# Step 8 — Share Notes

Endpoint:

```txt
POST /notes/{id}/share
```

Payload:

```json
{
  "share_with_email": "friend@gmail.com"
}
```

Validation:

* target user exists
* owner cannot share with self
* duplicate share prevented

---

# Step 9 — Version History Feature

# Get History

```txt
GET /notes/{id}/history
```

Returns all previous versions.

---

# Restore Old Version

```txt
POST /notes/{id}/restore/{version}
```

Flow:

* fetch selected version
* restore title/content
* update note

---

Because this demonstrates:

* Audit systems
* Real-world recovery
* State tracking
* Historical data handling
* Product thinking


---

# Step 10 — API Documentation

FastAPI automatically provides:

```txt
/openapi.json
/docs
```

This satisfies assignment requirements automatically.

---

# Step 11 — About Endpoint

Endpoint:

```txt
GET /about
```

Example:

```json
{
  "name": "Your Name",
  "email": "your@email.com",
  "my_features": {
    "Version History": "Tracks previous versions of notes and allows restoring them."
  }
}
```

---

# Step 12 — Security Best Practices

# Password Hashing

Use bcrypt.

Never store raw passwords.

---

# JWT Expiry

Use token expiration.

Example:

* 24 hours

---

# Environment Variables

Use:

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

# Step 13 — Error Handling

Professional projects handle edge cases.

## Register

* duplicate email
* invalid email
* weak password

## Login

* wrong credentials

## Notes

* unauthorized access
* note not found
* empty title

## Sharing

* share with self
* duplicate sharing
* non-existent user

---

# Step 14 — Docker

# Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# Step 15 — Deployment on Render

## Build Command

```txt
pip install -r requirements.txt
```

## Start Command

```txt
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

