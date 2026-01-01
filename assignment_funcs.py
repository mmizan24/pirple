import sqlite3  # For database operations
from typing import List, Tuple, Optional


# Function for the Artist attributedipt
def artist(name: Optional[str] = None) -> str:
    """Return the artist name. If name is not provided, prompt the user."""
    if name is None:
        name = input("Enter artist name: ").strip()
    return name

# Function for the Genre attribute
def genre(name: Optional[str] = None) -> str:
    """Return the genre. If name is not provided, prompt the user."""
    if name is None:
        name = input("Enter genre: ").strip()
    return name

# Function for the Year attribute
def year(y: Optional[int] = None) -> int:
    """Return the year as an int. If y is not provided, prompt the user and validate input."""
    if y is None:
        while True:
            try:
                y = int(input("Enter year: ").strip())
                break
            except ValueError:
                print("Please enter a valid integer for year.")
    return int(y)

# Extra Credit: Function returning a Boolean value
# This function checks if the song/album is considered a classic
def is_classic(value: Optional[bool] = None) -> bool:
    """Return a boolean. If value is not provided, ask the user (y/n)."""
    if value is None:
        val = input("Is it a classic? (y/n): ").strip().lower()
        return val in ("y", "yes", "true", "1")
    return bool(value)

# --- Database helper functions ---

def connect_db(db_path: str = "albums.db") -> sqlite3.Connection: # this is database connection
    """Connect to SQLite database and return the connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None: # create table
    """Create the albums table with a UNIQUE constraint on artist."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT UNIQUE NOT NULL,
            genre TEXT,
            year INTEGER,
            is_classic INTEGER
        )
        """
    )
    conn.commit()


def add_album(conn: sqlite3.Connection, artist_name: str, genre_name: str, year_val: int, classic: bool) -> bool:
    """Attempt to insert an album. Returns True if inserted, False if artist already exists."""
    try:
        with conn:
            conn.execute(
                "INSERT INTO albums (artist, genre, year, is_classic) VALUES (?, ?, ?, ?)",
                (artist_name, genre_name, int(year_val), 1 if classic else 0),
            )
        return True
    except sqlite3.IntegrityError:
        # Raised when UNIQUE constraint on artist is violated
        return False


def fetch_albums(conn: sqlite3.Connection) -> List[sqlite3.Row]:
    """Fetch all albums ordered by id."""
    cur = conn.execute("SELECT id, artist, genre, year, is_classic FROM albums ORDER BY id")
    return cur.fetchall()


def print_albums_table(rows: List[sqlite3.Row]) -> None:
    """Print rows in a nicely formatted table."""
    headers = ("ID", "Artist", "Genre", "Year", "Classic")
    # Convert rows to list of tuples and format classic
    table = [
        (r["id"], r["artist"], r["genre"] or "", r["year"] if r["year"] is not None else "", "Yes" if r["is_classic"] else "No")
        for r in rows
    ]

    # compute column widths
    cols = list(zip(*([headers] + table))) if table else list(zip(*([headers])))
    widths = [max(len(str(cell)) for cell in col) for col in cols]

    # format row function
    def fmt_row(row):
        return " | ".join(str(cell).ljust(w) for cell, w in zip(row, widths))

    # separator
    sep = "-+-".join("-" * w for w in widths)

    print(fmt_row(headers))
    print(sep)
    for row in table:
        print(fmt_row(row))


def add_album_interactive(conn: sqlite3.Connection) -> None:
    """Collect input via existing prompt functions and add to DB (skips duplicates)."""
    a = artist()
    g = genre()
    y = year()
    c = is_classic()

    inserted = add_album(conn, a, g, y, c)
    if inserted:
        print(f"Added '{a}' to the database.")
    else:
        print(f"Artist '{a}' already exists in the database. Skipping.")


# --- Main interactive flow ---
if __name__ == "__main__":
    conn = connect_db()
    init_db(conn)

    print("Album DB — add entries (artist must be unique).")
    while True:
        opt = input("Add new entry? (y/n): ").strip().lower()
        if opt in ("n", "no"):
            break
        if opt in ("y", "yes", ""):
            add_album_interactive(conn)
            continue
        print("Please enter 'y' or 'n'.")

    rows = fetch_albums(conn)
    print("\nCurrent database contents:")
    print_albums_table(rows)
    conn.close()