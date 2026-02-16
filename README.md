# ALX Backend — User Data

Backend track for **personal data handling**, **Basic Auth**, **Session Auth**, and a full **User Authentication Service** (Flask + SQLAlchemy + bcrypt). This README explains **what each folder and file does** and **how to run the exercises** so you can follow or redo them yourself.

---

## Repository structure

| Folder | Topic | What you'll practice |
|--------|--------|----------------------|
| `0x00-personal_data` | PII and logging | Filtering PII in logs, encrypting passwords |
| `0x01-Basic_authentication` | HTTP Basic Auth | API with Basic Auth, User model, file-based storage |
| `0x02-Session_authentication` | Session Auth | Cookies, session IDs, login/logout, optional DB/expiry |
| `0x03-user_authentication_service` | Full auth service | User/DB/Auth, registration, login, sessions, reset password |

---

## Prerequisites

- **Python 3.7+**
- **Flask** (and dependencies from each project’s `requirements.txt`)
- **bcrypt** for `0x03-user_authentication_service`
- **SQLAlchemy 1.3.x** for the auth service

---

## 0x00 — Personal data

**Problem:** Logs and databases often contain PII (emails, passwords, names). You must redact PII in logs and never store plain-text passwords. This project introduces filtered logging and password hashing.

### Files and what they solve

| File | Problem solved | How to run |
|------|----------------|------------|
| `filtered_logger.py` | Redact PII in log messages (e.g. mask email, password field) | Import and use a custom logger; log messages with "password", "email" etc. and see redacted output |
| `encrypt_password.py` | Hash a password (e.g. with bcrypt) for safe storage | `python3 encrypt_password.py` or call from REPL with a password |
| `main.py` | Demo of filtered logging / usage of the logger | `python3 main.py` |
| `main.sql` | Example SQL (e.g. safe handling of user data) | Run in MySQL if applicable |
| `user_data.csv` | Sample data for testing redaction/storage | Used by scripts or for manual tests |

### Doing the exercises yourself

1. Implement a logging filter that replaces patterns like `password=...` and `email=...` with `***`.
2. Use a strong hashing library (e.g. bcrypt) to hash passwords and compare with `checkpw` for verification.
3. Run `main.py` and confirm logs never show raw PII.

---

## 0x01 — Basic authentication

**Problem:** Protect API endpoints so only clients that send a valid username/password (HTTP Basic Auth) can access them. Users are stored in a file (no DB yet).

### Structure

```
0x01-Basic_authentication/
├── models/
│   ├── base.py    # Base model + file (de)serialization
│   └── user.py    # User model (email, password, etc.)
├── api/v1/
│   ├── app.py           # Flask app, before_request, auth
│   ├── auth/
│   │   ├── auth.py      # Base Auth class
│   │   └── basic_auth.py # Basic Auth (Authorization header, user lookup)
│   └── views/
│       ├── index.py     # /status, /stats
│       └── users.py     # CRUD for users
├── requirements.txt
└── main_0.py / main_1.py  # Runners or demos
```

### Files and what they solve

| File | Problem solved |
|------|----------------|
| `models/base.py` | Load/save JSON to file; base for all models |
| `models/user.py` | User with email, hashed password; save/load from file |
| `api/v1/auth/auth.py` | Base Auth: `require_auth`, `authorization_header`, `current_user` |
| `api/v1/auth/basic_auth.py` | Decode Basic header, find user by email, validate password |
| `api/v1/app.py` | Flask app; `@app.before_request` sets `request.current_user` from `auth.current_user(request)` |
| `api/v1/views/index.py` | `GET /api/v1/status`, `GET /api/v1/stats` |
| `api/v1/views/users.py` | `GET/POST/PUT/DELETE /api/v1/users` and `GET /api/v1/users/<id>`; support `id == "me"` for current user |

### Run

```bash
cd 0x01-Basic_authentication
pip install -r requirements.txt
API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```

Then:

- `GET /api/v1/status` — no auth
- `GET /api/v1/users` — requires Basic Auth (email:password)
- `GET /api/v1/users/me` — returns the authenticated user

### Doing the exercises yourself

1. Implement `BasicAuth`: extract `Authorization: Basic <base64>`, decode, get email/password, find user, validate password, set `current_user`.
2. Add `GET /api/v1/users/me`: if `<user_id> == "me"`, return `request.current_user` (or 404 if not authenticated).
3. Ensure all user endpoints use `@require_auth` and that unauthenticated requests get 401.

---

## 0x02 — Session authentication

**Problem:** For browser-based clients, session cookies are often better than sending Basic Auth every time. This project adds session creation, cookie-based lookup, optional expiration, and optional DB-backed sessions.

### Structure

```
0x02-Session_authentication/
├── models/
│   ├── base.py
│   ├── user.py
│   └── user_session.py   # Session stored in DB (optional task)
├── api/v1/
│   ├── app.py            # AUTH_TYPE → SessionAuth / SessionExpAuth / SessionDBAuth
│   ├── auth/
│   │   ├── auth.py       # session_cookie(request)
│   │   ├── session_auth.py      # in-memory session_id ↔ user_id
│   │   ├── session_exp_auth.py  # session with created_at + SESSION_DURATION
│   │   └── session_db_auth.py  # sessions in DB (UserSession)
│   └── views/
│       ├── session_auth.py # POST /auth_session/login, DELETE /auth_session/logout
│       └── ...
```

### Files and what they solve

| File | Problem solved |
|------|----------------|
| `api/v1/auth/session_auth.py` | Create session ID for user_id; look up user_id from session_id (in-memory dict) |
| `api/v1/auth/session_exp_auth.py` | Session with `created_at`; invalidate after `SESSION_DURATION` seconds |
| `api/v1/auth/session_db_auth.py` | Store sessions in DB (UserSession); create/destroy/lookup by session_id |
| `api/v1/auth/auth.py` | `session_cookie(request)` reads cookie name from `SESSION_NAME` env |
| `api/v1/app.py` | Exclude `/auth_session/login/` from auth; require either Basic or session cookie |
| `api/v1/views/session_auth.py` | Login (email/password → create session, set cookie); Logout (destroy session) |
| `models/user_session.py` | UserSession model (user_id, session_id) for SessionDBAuth |

### Run

```bash
cd 0x02-Session_authentication
pip install -r requirements.txt
AUTH_TYPE=session_auth API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
# Login:
curl -X POST http://localhost:5000/api/v1/auth_session/login -d "email=user@example.com" -d "password=pass"
# Use returned cookie for GET /api/v1/users/me
```

### Doing the exercises yourself

1. Implement `SessionAuth`: `create_session(user_id)`, `user_id_for_session_id(session_id)`, then `current_user(request)` using session cookie.
2. Add login view: validate email/password, create session, set cookie; add logout view: destroy session.
3. Add `SessionExpAuth`: store `{ user_id, created_at }`; in `user_id_for_session_id` return None if session expired.
4. Add `SessionDBAuth` and `UserSession`: persist sessions in DB and read/destroy from DB.

---

## 0x03 — User authentication service

**Problem:** Build a minimal but complete auth service: user model in DB, registration, login (session in DB), profile, logout, and reset-password flow. The app uses only the `Auth` (and optionally `DB`) interface, not raw DB access.

### Structure

```
0x03-user_authentication_service/
├── user.py    # SQLAlchemy User model (id, email, hashed_password, session_id, reset_token)
├── db.py      # DB class: add_user, find_user_by, update_user
├── auth.py    # Auth: register_user, valid_login, create_session, get_user_from_session_id,
│              # destroy_session, get_reset_password_token, update_password
├── app.py     # Flask routes: /, POST /users, POST /sessions, DELETE /sessions, GET /profile,
│              # POST /reset_password, PUT /reset_password
└── main.py    # End-to-end integration test (register, login, profile, logout, reset flow)
```

### Files and what they solve

| File | Problem solved |
|------|----------------|
| `user.py` | User table: id, email, hashed_password, session_id, reset_token |
| `db.py` | SQLite engine + session; add_user, find_user_by(kwargs), update_user(user_id, **kwargs) |
| `auth.py` | _hash_password, _generate_uuid; register_user, valid_login, create_session, get_user_from_session_id, destroy_session, get_reset_password_token, update_password |
| `app.py` | Routes: GET /, POST /users (register), POST /sessions (login, set session_id cookie), DELETE /sessions (logout), GET /profile (by cookie), POST /reset_password (get token), PUT /reset_password (update with token) |
| `main.py` | Integration test: register → wrong password → profile unlogged → login → profile logged → logout → reset token → update password → login with new password |

### Run

```bash
cd 0x03-user_authentication_service
pip install -r requirements.txt   # or pip install bcrypt flask sqlalchemy
python3 app.py
# In another terminal:
python3 main.py   # Should complete with no output (all asserts pass)
```

Example flows:

```bash
# Register
curl -X POST http://localhost:5000/users -d "email=bob@bob.com" -d "password=myPwd"

# Login (returns Set-Cookie: session_id=...)
curl -X POST http://localhost:5000/sessions -d "email=bob@bob.com" -d "password=myPwd" -v

# Profile (use cookie from login)
curl -X GET http://localhost:5000/profile -b "session_id=<session_id>"

# Reset password
curl -X POST http://localhost:5000/reset_password -d "email=bob@bob.com"
curl -X PUT http://localhost:5000/reset_password -d "email=bob@bob.com" -d "reset_token=<token>" -d "new_password=newPwd"
```

### Doing the exercises yourself

1. **user.py:** Define User with SQLAlchemy; columns as in spec.
2. **db.py:** add_user (insert and return User), find_user_by (filter by kwargs, raise NoResultFound/InvalidRequestError), update_user (find, update attributes, commit; raise ValueError for invalid keys).
3. **auth.py:** Hash password (bcrypt), register (check exists, hash, add_user), valid_login (find user, checkpw), create_session (uuid, update user.session_id), get_user_from_session_id, destroy_session (set session_id to None), get_reset_password_token (set user.reset_token), update_password (find by token, hash new password, clear token).
4. **app.py:** Implement each route; use only Auth (and User/DB via Auth), return correct status codes and JSON.
5. **main.py:** Use `requests` to call each endpoint and assert status and body.

---

## Quick reference

| Goal | Where | Command / note |
|------|--------|------------------|
| Filter PII in logs | 0x00-personal_data | Implement filter in `filtered_logger.py`, run `main.py` |
| Encrypt password | 0x00-personal_data | `encrypt_password.py` |
| Basic Auth API | 0x01-Basic_authentication | `pip install -r requirements.txt`, `python3 -m api.v1.app` |
| Session Auth API | 0x02-Session_authentication | Set `AUTH_TYPE=session_auth`, run app, use login/logout views |
| Full auth service | 0x03-user_authentication_service | Run `app.py`, then `main.py` for integration test |

Each subfolder has its own `README.md` with detailed task lists; this file is the high-level map of **what each project and file is for** and **how to run and redo the exercises**.
