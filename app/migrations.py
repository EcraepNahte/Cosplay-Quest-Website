import sqlite3
from .database import SQLALCHEMY_DATABASE_URL
import os

MIGRATION_FLAG_FILE = "migration_completed.flag"

def run_migrations():
    if os.path.exists(MIGRATION_FLAG_FILE):
        print("Migrations have already been applied.")
        return

    # Extract the database file path from the URL
    db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the column exists
    cursor.execute("PRAGMA table_info(feedback)")
    columns = [column[1] for column in cursor.fetchall()]

    if "created_at" not in columns:
        # Create a new table with the desired schema
        cursor.execute("""
        CREATE TABLE new_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            email VARCHAR,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Copy data from the old table to the new table
        cursor.execute("INSERT INTO new_feedback (id, name, email, message) SELECT id, name, email, message FROM feedback")

        # Drop the old table
        cursor.execute("DROP TABLE feedback")

        # Rename the new table to the original table name
        cursor.execute("ALTER TABLE new_feedback RENAME TO feedback")

        print("Migration completed: 'created_at' column added to the feedback table.")
    else:
        print("Column 'created_at' already exists. No migration needed.")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Create a flag file to indicate that migrations have been run
    with open(MIGRATION_FLAG_FILE, "w") as flag_file:
        flag_file.write("Migrations completed")

    print("Migration flag created. Migrations will not run again.")

if __name__ == "__main__":
    run_migrations()