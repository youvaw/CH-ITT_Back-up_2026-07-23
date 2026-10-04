def create_test_table(db):

    db.execute("""
    CREATE TABLE IF NOT EXISTS test_table(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
"""
AetherMind Database Test
File: database/test_table.py
"""

from .manager import DatabaseManager


def main():

    db = DatabaseManager()

    print("=" * 50)
    print("AetherMind Database Test")
    print("=" * 50)

    # Create Test Table
    db.execute("""
    CREATE TABLE IF NOT EXISTS test_table(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    print("✅ Test Table Created")

    # Insert Test Data
    db.execute("""
    INSERT INTO test_table(name, status)
    VALUES(?, ?)
    """, ("Aethira", "Working"))

    print("✅ Test Data Inserted")

    # Read Data
    rows = db.fetchall("""
    SELECT * FROM test_table
    """)

    print("\nDatabase Records\n")

    for row in rows:
        print(dict(row))

    print("\n✅ Database Working Successfully")

    db.close()


if __name__ == "__main__":
    main()
    
