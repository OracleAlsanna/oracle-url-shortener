# oracle — Command-Line URL Shortener

> **Part 1 of 5** in a series building toward a full URL analytics platform.

`oracle` is a lightweight CLI tool that maps long URLs to names drawn from
FromSoftware titles — Dark Souls, Bloodborne, Elden Ring, Sekiro, and more.
All mappings are persisted locally in a SQLite database. No network calls, no
dependencies beyond the Python standard library.

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
Shorten a URL. Prints the assigned name.
If the URL was already shortened, returns the existing name instead of
creating a duplicate.

```
$ oracle create https://www.example.com/some/very/long/path?query=value
Shortened: oracle/Malenia

$ oracle create https://www.example.com/some/very/long/path?query=value
Already exists: oracle/Malenia
```

### `oracle get <name>`
Retrieve the original URL for a given name.

```
$ oracle get Malenia
Malenia  ->  https://www.example.com/some/very/long/path?query=value
```

### `oracle list`
Display all stored names and their URLs in a formatted table.

```
$ oracle list
CODE       ORIGINAL URL                                               CREATED AT
---------  ---------------------------------------------------------  --------------------------
Malenia    https://www.example.com/some/very/long/path?query=value   2026-03-10T12:00:00+00:00
Gehrman    https://docs.python.org/3/library/sqlite3.html            2026-03-10T12:05:00+00:00
```

### `oracle delete <name>`
Remove a mapping from the database.

```
$ oracle delete Malenia
Deleted: Malenia
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
    ├── names.py      # FromSoftware name pool
    └── shortener.py  # Random name selection with collision handling
```

---

## How Names Are Generated

When a URL is shortened, `oracle` randomly selects a name from a curated
pool of characters, bosses, and NPCs drawn from FromSoftware titles including
Dark Souls I–III, Bloodborne, Elden Ring, Sekiro, and Demon's Souls. 
If the selected name is already taken, a new one is chosen at random until a free name is found.

---

## Roadmap (5-Part Series)

| Part | Description |
|------|-------------|
| **1 — oracle** (this project) | Core CLI: create, get, list, delete |
| 2 — REST API | Expose oracle over HTTP with FastAPI |
| 3 — Web Dashboard | Frontend UI for managing and viewing links |
| 4 — Analytics Engine | Track clicks with timestamp, referrer, and device data |
| 5 — Cache & Rate Limiter | Redis caching and rate limiting for scale |
