import argparse
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

from oracle import db, shortener


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _validate_url(url: str) -> None:
    """Raise SystemExit with a friendly message if the URL is malformed."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        print(f"Error: '{url}' is not a valid URL. Must start with http:// or https://")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_create(args: argparse.Namespace) -> None:
    url = args.url
    _validate_url(url)

    existing = db.get_by_url(url)
    if existing:
        print(f"Already exists: oracle/{existing['code']}")
        return

    if args.code:
        try:
            shortener.validate_custom_code(args.code)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        if db.code_exists(args.code):
            print(f"Error: code '{args.code}' is already taken.")
            sys.exit(1)
        code = args.code
    else:
        code = shortener.generate_code(db.code_exists)

    expires_at = None
    if args.expires_in is not None:
        if args.expires_in <= 0:
            print("Error: --expires-in must be a positive number of hours.")
            sys.exit(1)
        expires_at = (
            datetime.now(timezone.utc) + timedelta(hours=args.expires_in)
        ).isoformat()

    row = db.insert(code, url, expires_at=expires_at)
    print(f"Shortened: oracle/{row['code']}")
    if expires_at:
        print(f"Expires at: {expires_at}")


def cmd_get(args: argparse.Namespace) -> None:
    row = db.get_by_code(args.code)
    if not row:
        print(f"Error: No entry found for code '{args.code}'")
        sys.exit(1)
    if row["expires_at"] and datetime.now(timezone.utc) > datetime.fromisoformat(row["expires_at"]):
        print(f"Error: code '{args.code}' has expired.")
        sys.exit(1)
    print(f"{row['code']}  ->  {row['original_url']}")


def cmd_list(_args: argparse.Namespace) -> None:
    rows = db.list_all()
    if not rows:
        print("No links stored yet. Use 'oracle create <url>' to add one.")
        return

    # Build columns: code, original_url, created_at
    headers = ("CODE", "ORIGINAL URL", "CREATED AT")
    data = [(r["code"], r["original_url"], r["created_at"]) for r in rows]

    col_widths = [
        max(len(headers[i]), max(len(row[i]) for row in data))
        for i in range(len(headers))
    ]

    def fmt_row(cells):
        return "  ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(cells))

    separator = "  ".join("-" * w for w in col_widths)

    print(fmt_row(headers))
    print(separator)
    for row in data:
        print(fmt_row(row))


def cmd_delete(args: argparse.Namespace) -> None:
    removed = db.delete(args.code)
    if not removed:
        print(f"Error: No entry found for code '{args.code}'")
        sys.exit(1)
    print(f"Deleted: {args.code}")


# ---------------------------------------------------------------------------
# Parser setup
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="oracle",
        description="A command-line URL shortener backed by SQLite.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    # create
    p_create = subparsers.add_parser("create", help="Shorten a URL")
    p_create.add_argument("url", help="The URL to shorten")
    p_create.add_argument(
        "--code", default=None, help="Use a custom code instead of a random one (3-20 alphanumeric characters)"
    )
    p_create.add_argument(
        "--expires-in", type=int, default=None, metavar="HOURS",
        help="Expire the link after this many hours",
    )
    p_create.set_defaults(func=cmd_create)

    # get
    p_get = subparsers.add_parser("get", help="Look up the original URL for a short code")
    p_get.add_argument("code", help="The short code to look up")
    p_get.set_defaults(func=cmd_get)

    # list
    p_list = subparsers.add_parser("list", help="List all stored short codes")
    p_list.set_defaults(func=cmd_list)

    # delete
    p_delete = subparsers.add_parser("delete", help="Remove a short code")
    p_delete.add_argument("code", help="The short code to remove")
    p_delete.set_defaults(func=cmd_delete)

    return parser


def main() -> None:
    db.init_db()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
