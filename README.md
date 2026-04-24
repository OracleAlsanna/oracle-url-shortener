# oracle — Command-Line URL Shortener

> **Part 1 of 5** in a series building toward a full URL analytics platform.

`oracle` is a lightweight CLI tool that maps long URLs to short alphanumeric
codes. All mappings are persisted locally in a SQLite database. No network
calls, no dependencies beyond the Python standard library.

---

## Setup

**Requirements:** Python 3.10 or newer.

```bash
# Clone the repository, then:
cd oracle-url-shortener

# Run directly
python main.py <command> [args]

# Or install as an editable package for the `oracle` command
pip install -e .
oracle <command> [args]
```

The database is created automatically on first run at `~/.oracle/db.sqlite3`.

---

## Commands

### `oracle create <url>`
Shorten a URL. Prints the assigned code.
If the URL was already shortened, returns the existing code instead of
creating a duplicate.

```
$ oracle create https://www.example.com/some/very/long/path?query=value
Shortened: oracle/X7K2

$ oracle create https://www.example.com/some/very/long/path?query=value
Already exists: oracle/X7K2
```

### `oracle get <code>`
Retrieve the original URL for a given code.

```
$ oracle get X7K2
X7K2  ->  https://www.example.com/some/very/long/path?query=value
```

### `oracle list`
Display all stored codes and their URLs in a formatted table.

```
$ oracle list
CODE  ORIGINAL URL                                               CREATED AT
----  ---------------------------------------------------------  --------------------------
X7K2  https://www.example.com/some/very/long/path?query=value   2026-03-10T12:00:00+00:00
M3PQ  https://docs.python.org/3/library/sqlite3.html            2026-03-10T12:05:00+00:00
```

### `oracle delete <code>`
Remove a mapping from the database.

```
$ oracle delete X7K2
Deleted: X7K2
```

---

## Project Structure

```
oracle-url-shortener/
├── main.py           # Entry point
├── requirements.txt  # No third-party dependencies
├── README.md
└── oracle/
    ├── __init__.py
    ├── cli.py        # Argument parsing and command routing (argparse)
    ├── db.py         # Database initialization and CRUD (sqlite3)
    └── shortener.py  # Random code generation with collision handling
```

---

## How Codes Are Generated

When a URL is shortened, `oracle` generates a random 4-character alphanumeric
code drawn from uppercase letters and digits (A–Z, 0–9). If the generated code
is already taken, a new one is generated until a free code is found.

---

## Roadmap (5-Part Series)

| Part | Description |
|------|-------------|
| **1 — oracle** (this project) | Core CLI: create, get, list, delete |
| 2 — REST API | Expose oracle over HTTP with FastAPI |
| 3 — Web Dashboard | Frontend UI for managing and viewing links |
| 4 — Analytics Engine | Track clicks with timestamp, referrer, and device data |
| 5 — Cache & Rate Limiter | Redis caching and rate limiting for scale |
