import os
import sys
import sqlite3
from datetime import datetime


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# FILE INDEX
# ============================================================

class FileIndex:
    """
    MYX File Index

    Responsibilities:
        - Store discovered file metadata
        - Update existing file records
        - Search files by name
        - Search files by category
        - Search files by extension
        - Search files by folder
        - Remove files that no longer exist

    Important:
        This module does NOT read file contents.
        This module does NOT modify user files.
        This module only stores metadata.
    """

    def __init__(self, database_path=None):

        if database_path is None:
            data_directory = os.path.join(
                PROJECT_ROOT,
                "data"
            )

            os.makedirs(
                data_directory,
                exist_ok=True
            )

            database_path = os.path.join(
                data_directory,
                "myx_file_index.db"
            )

        self.database_path = os.path.abspath(
            database_path
        )

        self.connection = None

        print("[FileIndex] Initialized")
        print(
            f"[FileIndex] Database: "
            f"{self.database_path}"
        )

        self.connect()
        self.create_tables()

    # ========================================================
    # DATABASE
    # ========================================================

    def connect(self):

        self.connection = sqlite3.connect(
            self.database_path
        )

        self.connection.row_factory = sqlite3.Row

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS files (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                normalized_name TEXT NOT NULL,

                path TEXT NOT NULL UNIQUE,

                folder TEXT NOT NULL,

                extension TEXT,

                category TEXT,

                size_bytes INTEGER,

                modified_timestamp REAL,

                discovered_at REAL NOT NULL,

                discovery_source TEXT

            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_files_normalized_name

            ON files(normalized_name)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_files_category

            ON files(category)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_files_extension

            ON files(extension)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_files_folder

            ON files(folder)
            """
        )

        self.connection.commit()

    # ========================================================
    # NORMALIZATION
    # ========================================================

    def normalize(self, value):

        if value is None:
            return ""

        return " ".join(
            str(value)
            .strip()
            .lower()
            .split()
        )

    # ========================================================
    # ADD / UPDATE FILE
    # ========================================================

    def add_file(self, file_record):

        if not file_record:
            return False

        path = os.path.normpath(
            str(
                file_record.get(
                    "path",
                    ""
                )
            ).strip()
        )

        if not path:
            return False

        name = str(
            file_record.get(
                "name",
                ""
            )
        ).strip()

        if not name:
            name = os.path.basename(path)

        folder = file_record.get(
            "folder"
        )

        if folder:
            folder = os.path.normpath(
                str(folder).strip()
            )
        else:
            folder = os.path.dirname(path)

        extension = str(
            file_record.get(
                "extension",
                ""
            )
        ).strip().lower()

        category = str(
            file_record.get(
                "category",
                "other"
            )
        ).strip().lower()

        size_bytes = file_record.get(
            "size_bytes"
        )

        modified_timestamp = file_record.get(
            "modified_timestamp"
        )

        discovery_source = str(
            file_record.get(
                "discovery_source",
                "filesystem"
            )
        ).strip()

        discovered_at = (
            datetime.now().timestamp()
        )

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO files (

                name,
                normalized_name,
                path,
                folder,
                extension,
                category,
                size_bytes,
                modified_timestamp,
                discovered_at,
                discovery_source

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(path)
            DO UPDATE SET

                name = excluded.name,

                normalized_name =
                    excluded.normalized_name,

                folder =
                    excluded.folder,

                extension =
                    excluded.extension,

                category =
                    excluded.category,

                size_bytes =
                    excluded.size_bytes,

                modified_timestamp =
                    excluded.modified_timestamp,

                discovered_at =
                    excluded.discovered_at,

                discovery_source =
                    excluded.discovery_source
            """,
            (
                name,
                self.normalize(name),
                path,
                folder,
                extension,
                category,
                size_bytes,
                modified_timestamp,
                discovered_at,
                discovery_source,
            )
        )

        self.connection.commit()

        return True

    # ========================================================
    # BULK INDEX
    # ========================================================

    def index_files(self, file_records):

        if not file_records:
            return 0

        count = 0

        for file_record in file_records:

            try:

                if self.add_file(
                    file_record
                ):
                    count += 1

            except Exception as error:

                print(
                    "[FileIndex] "
                    f"Unable to index file: "
                    f"{error}"
                )

        return count

    # ========================================================
    # SEARCH BY NAME
    # ========================================================

    def search_name(
        self,
        query,
        limit=20
    ):

        query = self.normalize(query)

        if not query:
            return []

        pattern = f"%{query}%"

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM files

            WHERE normalized_name LIKE ?

            ORDER BY

                CASE

                    WHEN normalized_name = ?
                    THEN 0

                    ELSE 1

                END,

                name COLLATE NOCASE

            LIMIT ?
            """,
            (
                pattern,
                query,
                limit,
            )
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    # ========================================================
    # SEARCH BY CATEGORY
    # ========================================================

    def search_category(
        self,
        category,
        limit=50
    ):

        category = self.normalize(
            category
        )

        if not category:
            return []

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM files

            WHERE category = ?

            ORDER BY name COLLATE NOCASE

            LIMIT ?
            """,
            (
                category,
                limit,
            )
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    # ========================================================
    # SEARCH BY EXTENSION
    # ========================================================

    def search_extension(
        self,
        extension,
        limit=50
    ):

        extension = self.normalize(
            extension
        )

        if not extension:
            return []

        if not extension.startswith("."):
            extension = "." + extension

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM files

            WHERE extension = ?

            ORDER BY name COLLATE NOCASE

            LIMIT ?
            """,
            (
                extension,
                limit,
            )
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    # ========================================================
    # SEARCH BY FOLDER
    # ========================================================

    def search_folder(
        self,
        folder,
        limit=50
    ):

        folder = os.path.normpath(
            str(folder).strip()
        )

        if not folder:
            return []

        pattern = folder + "%"

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM files

            WHERE path LIKE ?

            ORDER BY path COLLATE NOCASE

            LIMIT ?
            """,
            (
                pattern,
                limit,
            )
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    # ========================================================
    # COUNT
    # ========================================================

    def count_files(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM files
            """
        )

        return cursor.fetchone()[0]

    # ========================================================
    # CATEGORY STATISTICS
    # ========================================================

    def count_categories(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                category,
                COUNT(*) AS count

            FROM files

            GROUP BY category

            ORDER BY count DESC
            """
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    # ========================================================
    # REMOVE MISSING FILES
    # ========================================================

    def remove_missing_files(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT id, path
            FROM files
            """
        )

        rows = cursor.fetchall()

        removed = 0

        for row in rows:

            path = row["path"]

            if not os.path.exists(path):

                cursor.execute(
                    """
                    DELETE FROM files
                    WHERE id = ?
                    """,
                    (
                        row["id"],
                    )
                )

                removed += 1

        self.connection.commit()

        return removed

    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        if self.connection is not None:

            self.connection.close()

            self.connection = None


# ============================================================
# TEST
# ============================================================

def run_test():

    print("\n==========================================")
    print("          MYX FILE INDEX TEST")
    print("==========================================")

    # --------------------------------------------------------
    # Temporary test database
    # --------------------------------------------------------

    test_database = os.path.join(
        PROJECT_ROOT,
        "myx_file_index_test.db"
    )

    if os.path.exists(
        test_database
    ):
        os.remove(
            test_database
        )

    index = FileIndex(
        database_path=test_database
    )

    # --------------------------------------------------------
    # Fake test records
    # --------------------------------------------------------

    test_files = [

        {
            "name": "Python Tutorial.pdf",

            "path":
                r"C:\Users\AVISHKAR\Documents"
                r"\Python Tutorial.pdf",

            "folder":
                r"C:\Users\AVISHKAR\Documents",

            "extension": ".pdf",

            "category": "pdf",

            "size_bytes": 120000,

            "modified_timestamp": 1000,

            "discovery_source":
                "filesystem",
        },

        {
            "name": "EV Project.docx",

            "path":
                r"C:\Users\AVISHKAR\Documents"
                r"\EV Project.docx",

            "folder":
                r"C:\Users\AVISHKAR\Documents",

            "extension": ".docx",

            "category": "document",

            "size_bytes": 220000,

            "modified_timestamp": 2000,

            "discovery_source":
                "filesystem",
        },

        {
            "name": "CHITT AI.py",

            "path":
                r"C:\Users\AVISHKAR\Projects"
                r"\CHITT AI.py",

            "folder":
                r"C:\Users\AVISHKAR\Projects",

            "extension": ".py",

            "category": "code",

            "size_bytes": 50000,

            "modified_timestamp": 3000,

            "discovery_source":
                "filesystem",
        },
    ]

    # --------------------------------------------------------
    # TEST 1
    # --------------------------------------------------------

    indexed = index.index_files(
        test_files
    )

    print(
        f"\nFiles indexed: {indexed}"
    )

    assert indexed == 3

    print(
        "INDEX INSERT TEST: PASS"
    )

    # --------------------------------------------------------
    # TEST 2
    # --------------------------------------------------------

    total = index.count_files()

    print(
        f"Total indexed: {total}"
    )

    assert total == 3

    print(
        "COUNT TEST: PASS"
    )

    # --------------------------------------------------------
    # TEST 3
    # --------------------------------------------------------

    results = index.search_name(
        "python tutorial"
    )

    print("\nName search:")

    for result in results:

        print(
            f"  {result['name']} "
            f"-> {result['path']}"
        )

    assert len(results) == 1

    assert (
        results[0]["name"]
        == "Python Tutorial.pdf"
    )

    print(
        "NAME SEARCH TEST: PASS"
    )

    # --------------------------------------------------------
    # TEST 4
    # --------------------------------------------------------

    results = index.search_category(
        "pdf"
    )

    print("\nPDF search:")

    for result in results:

        print(
            f"  {result['name']} "
            f"-> {result['path']}"
        )

    assert len(results) == 1

    print(
        "CATEGORY SEARCH TEST: PASS"
    )

    # --------------------------------------------------------
    # TEST 5
    # --------------------------------------------------------

    results = index.search_extension(
        ".py"
    )

    print("\nPython files:")

    for result in results:

        print(
            f"  {result['name']} "
            f"-> {result['path']}"
        )

    assert len(results) == 1

    print(
        "EXTENSION SEARCH TEST: PASS"
    )

    # --------------------------------------------------------
    # TEST 6
    # --------------------------------------------------------

    results = index.search_folder(
        r"C:\Users\AVISHKAR\Documents"
    )

    print("\nDocuments folder:")

    for result in results:

        print(
            f"  {result['name']}"
        )

    assert len(results) == 2

    print(
        "FOLDER SEARCH TEST: PASS"
    )

    # --------------------------------------------------------
    # TEST 7
    # --------------------------------------------------------

    statistics = index.count_categories()

    print("\nCategory statistics:")

    for item in statistics:

        print(
            f"  {item['category']}: "
            f"{item['count']}"
        )

    assert isinstance(
        statistics,
        list
    )

    assert len(statistics) == 3

    print(
        "STATISTICS TEST: PASS"
    )

    # --------------------------------------------------------
    # CLOSE
    # --------------------------------------------------------

    index.close()

    # --------------------------------------------------------
    # DELETE TEST DATABASE
    # --------------------------------------------------------

    if os.path.exists(
        test_database
    ):
        os.remove(
            test_database
        )

    print("\n==========================================")
    print("       FILE INDEX TEST PASSED")
    print("==========================================")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_test()
    
