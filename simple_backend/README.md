# simple-backend

A minimal Flask REST API with auth, user, database, and API modules.

## Structure
```
simple_backend/
├── app.py              ← entry point
├── requirements.txt
├── auth/
│   └── auth.py         ← register, login, logout, verify (JWT)
├── user/
│   └── user.py         ← profile CRUD
├── database/
│   └── db.py           ← SQLite helpers, init_db
└── api/
    └── routes.py       ← task CRUD endpoints
```

## Endpoints

### Auth  /auth
| Method | Route       | Description        |
|--------|-------------|--------------------|
| POST   | /register   | Register new user  |
| POST   | /login      | Login, get token   |
| POST   | /logout     | Logout             |
| GET    | /verify     | Verify JWT token   |

### User  /user
| Method | Route          | Description        |
|--------|----------------|--------------------|
| GET    | /profile       | Get own profile    |
| PUT    | /profile       | Update email       |
| GET    | /all           | List all users     |
| DELETE | /<user_id>     | Delete user        |

### API  /api
| Method | Route              | Description        |
|--------|--------------------|--------------------|
| GET    | /health            | Health check       |
| GET    | /tasks             | List tasks         |
| POST   | /tasks             | Create task        |
| PUT    | /tasks/<id>        | Update task status |
| DELETE | /tasks/<id>        | Delete task        |

## Run
```bash
pip install -r requirements.txt
python app.py
```
