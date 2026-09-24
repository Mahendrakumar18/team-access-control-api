# Team Access Control API

A backend REST API built with **FastAPI** and **PostgreSQL** for managing users, teams, team memberships, authentication, and role-based access control.

## Features

- User registration and login
- JWT-based authentication
- Secure password hashing using bcrypt
- Team management
- Team membership management
- Role-based access control (RBAC)
- Permission checking based on team roles
- Admin-only membership management
- PostgreSQL database integration
- Interactive Swagger API documentation

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- bcrypt
- Pydantic
- Uvicorn
- Git & GitHub

## Roles

The API supports four team roles:

| Role | Level |
|------|------:|
| Viewer | 1 |
| Member | 2 |
| Manager | 3 |
| Admin | 4 |

Higher-level roles have the permissions of lower-level roles.

## Authentication

The API uses JWT bearer tokens for authentication.

### Register

```http
POST /auth/register


## Running Tests

Activate the virtual environment and run:

```bash
python -m pytest -q
```

Expected result:

```text
7 passed
```
