0x01. Basic authentication
==========================

Simple HTTP API for playing with the `User` model, protected with **HTTP Basic Authentication**.

Tasks
-----

### 1. What does `models/base.py` do?

It is the **base for all models** of the API: it handles **serialization to/from a file** (e.g. JSON) so user data can be stored and loaded without a database. Other models inherit from it.

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x01-Basic_authentication`
-   File: `models/base.py`

### 2. What does `models/user.py` do?

It defines the **User model**: typically `email`, hashed `password`, and methods to save/load from the file. Used by the API to identify and validate users for Basic Auth.

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x01-Basic_authentication`
-   File: `models/user.py`

### 3. What does `api/v1/app.py` do?

It is the **entry point** of the Flask API: creates the app, registers blueprints, and runs **`@app.before_request`** to set `request.current_user` by calling `auth.current_user(request)`. Unauthenticated requests to protected routes get 401.

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x01-Basic_authentication`
-   File: `api/v1/app.py`

### 4. What does `api/v1/views/index.py` do?

It defines the **basic endpoints**: `GET /api/v1/status` (API status) and `GET /api/v1/stats` (e.g. count of users). Usually these do not require authentication.

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x01-Basic_authentication`
-   File: `api/v1/views/index.py`

### 5. What does `api/v1/views/users.py` do?

It defines **all user CRUD endpoints**: list users, get one user by ID, create, update, delete. It also handles the special case **`GET /api/v1/users/me`**: when the path parameter is `"me"`, it returns the **authenticated user** (from `request.current_user`) instead of 404 if not logged in.

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x01-Basic_authentication`
-   File: `api/v1/views/users.py`

### 6. What does `api/v1/auth/auth.py` do?

It defines the **base Auth class**: methods like `require_auth(path, excluded_paths)`, `authorization_header(request)`, and `current_user(request)`. Basic Auth and other auth mechanisms inherit from it.

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x01-Basic_authentication`
-   File: `api/v1/auth/auth.py`

### 7. What does `api/v1/auth/basic_auth.py` do?

It implements **Basic authentication**: decodes the `Authorization: Basic <base64>` header to get email and password, finds the user by email, validates the password, and returns the user as `current_user`. Used when the client sends credentials on each request.

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x01-Basic_authentication`
-   File: `api/v1/auth/basic_auth.py`

### 8. What do `main_0.py` and `main_1.py` do?

They are **runner or demo scripts** that start the API or test it (e.g. run the app on a given host/port). Use them to start the server or run quick checks. Run: `API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app` (see Run section below).

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x01-Basic_authentication`
-   File: `main_0.py`, `main_1.py`

---

## Files (overview)

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


## Setup

```
$ pip3 install -r requirements.txt
```


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)
