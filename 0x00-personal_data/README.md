0x00. Personal data
===================

This project practices **handling personal data safely**: filtering PII (personally identifiable information) out of logs and encrypting passwords so they are never stored or logged in plain text.

Tasks
-----

### 1. What does `filtered_logger.py` do?

It provides a **logging filter** (or custom formatter) that **redacts PII** from log messages before they are written. For example, it masks fields like `password=...` and `email=...` so that logs never contain real passwords or emails. You implement the filter and attach it to a logger. Run: Use from your app or from `main.py`; log a message that contains "password" or "email" and confirm the output shows redacted values (e.g. `***`).

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x00-personal_data`
-   File: `filtered_logger.py`

### 2. What does `filtered_logger_mine.py` do?

It is an **alternate or personal version** of the filtered logger (same idea as `filtered_logger.py`): redact PII in log output. Run: Same as above; use whichever module your project expects.

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x00-personal_data`
-   File: `filtered_logger_mine.py`

### 3. What does `encrypt_password.py` do?

It **hashes a password** (e.g. using bcrypt) so it can be stored safely. Typically it defines a function that takes a plain-text password and returns the hashed bytes or string. Never store or log the raw password. Run: `python3 encrypt_password.py` or call the hash function from REPL with a test password.

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x00-personal_data`
-   File: `encrypt_password.py`

### 4. What does `main.py` do?

It is a **demo script** that uses the filtered logger (and optionally other utilities) to show how log messages are redacted when they contain PII. Run: `python3 main.py` and check that no real PII appears in the console.

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x00-personal_data`
-   File: `main.py`

### 5. What does `main.sql` do?

It contains **sample SQL** or instructions related to handling user/personal data in a database (e.g. safe queries or schema). Run: Execute in MySQL if applicable.

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x00-personal_data`
-   File: `main.sql`

### 6. What is `user_data.csv`?

**Sample data** (e.g. names, emails) used to test redaction, import scripts, or examples. Do not commit real user data.

**Repo:**

-   GitHub repository: `alx-backend-user-data`
-   Directory: `0x00-personal_data`
-   File: `user_data.csv`

---

**How to do the exercises yourself**

1. Implement a logging filter that detects and replaces PII patterns (e.g. `password=.*`, `email=.*`) with a placeholder like `***`.
2. Use a strong hashing library (e.g. bcrypt) to hash passwords; use `checkpw` for verification.
3. Run `main.py` and ensure logs never show raw passwords or emails.
