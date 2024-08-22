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
    cursor.execute("PRAGMA table_info(beta_signup)")
    columns = [column[1] for column in cursor.fetchall()]

    if "will_cosplay" not in columns or "character" not in columns:
        # Create a new table with the desired schema
        cursor.execute("""
        CREATE TABLE new_beta_signup (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            email VARCHAR,
            device_os VARCHAR,
            next_con VARCHAR,
            next_con_date TIMESTAMP,
            will_cosplay BOOLEAN,
            character VARCHAR,
            source_media VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Copy data from the old table to the new table
        cursor.execute("INSERT INTO new_beta_signup (id, name, email, device_os, next_con, created_at) SELECT id, name, email, device_os, next_con, created_at FROM beta_signup")

        # Drop the old table
        cursor.execute("DROP TABLE beta_signup")

        # Rename the new table to the original table name
        cursor.execute("ALTER TABLE new_beta_signup RENAME TO beta_signup")

        print("Migration completed: 'will_cosplay', 'character', 'source_media' column added to the beta_signup table.")
    else:
        print("Migration completed: 'will_cosplay', 'character', 'source_media' already exist in the beta_signup table.")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Create a flag file to indicate that migrations have been run
    with open(MIGRATION_FLAG_FILE, "w") as flag_file:
        flag_file.write("Migrations completed")

    print("Migration flag created. Migrations will not run again.")

if __name__ == "__main__":
    run_migrations()