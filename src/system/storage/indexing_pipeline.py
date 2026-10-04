import os
import sys
import time
import inspect


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# MYX SYSTEM IMPORTS
# ============================================================

from src.system.storage.storage_discovery import StorageDiscovery
from src.system.storage.folder_discovery import FolderDiscovery
from src.system.storage.file_discovery import FileDiscovery
from src.system.storage.file_index import FileIndex


# ============================================================
# INDEXING PIPELINE
# ============================================================

class IndexingPipeline:
    """
    MYX Storage/File Indexing Pipeline

    Pipeline:

        Storage Discovery
                â†“
        Folder Discovery
                â†“
        File Discovery
                â†“
        File Index
                â†“
        Searchable File Database

    Important:
        This class does NOT hard-code individual files.

    It works with the discovery modules and the database index.
    """

    def __init__(
        self,
        storage_discovery=None,
        folder_discovery=None,
        file_discovery=None,
        file_index=None,
    ):

        self.storage_discovery = (
            storage_discovery
            if storage_discovery is not None
            else StorageDiscovery()
        )

        self.folder_discovery = (
            folder_discovery
            if folder_discovery is not None
            else FolderDiscovery()
        )

        self.file_discovery = (
            file_discovery
            if file_discovery is not None
            else FileDiscovery()
        )

        self.file_index = (
            file_index
            if file_index is not None
            else FileIndex()
        )

        print("[IndexingPipeline] Initialized")


    # ========================================================
    # FILE DISCOVERY
    # ========================================================

    def discover_files(
        self,
        folder_path,
        recursive=False,
        max_files=1000,
    ):
        """
        Discover files using the real FileDiscovery API.

        Current FileDiscovery API:
            discover_folder()
            get_file_category()
        """

        folder_path = os.path.abspath(
            os.path.expanduser(str(folder_path))
        )

        if not os.path.isdir(folder_path):
            print(
                f"[Pipeline] Invalid folder: {folder_path}"
            )
            return []

        try:

            discover_method = getattr(
                self.file_discovery,
                "discover_folder",
                None,
            )

            if discover_method is None:
                raise AttributeError(
                    "FileDiscovery.discover_folder() "
                    "was not found."
                )

            # ------------------------------------------------
            # Adapt to the actual method signature.
            # This prevents unnecessary failures if optional
            # parameters differ between versions.
            # ------------------------------------------------

            try:

                signature = inspect.signature(
                    discover_method
                )

                parameters = signature.parameters

                kwargs = {}

                if "recursive" in parameters:
                    kwargs["recursive"] = recursive

                if "max_files" in parameters:
                    kwargs["max_files"] = max_files

                result = discover_method(
                    folder_path,
                    **kwargs,
                )

            except (TypeError, ValueError):

                # Fallback for implementations that don't expose
                # a usable signature.

                try:
                    result = discover_method(
                        folder_path,
                        recursive,
                        max_files,
                    )

                except TypeError:
                    result = discover_method(
                        folder_path
                    )

            if result is None:
                return []

            # ------------------------------------------------
            # Normalize the result to a list.
            # ------------------------------------------------

            if isinstance(result, list):
                files = result

            elif isinstance(result, tuple):
                files = list(result)

            elif isinstance(result, set):
                files = list(result)

            else:
                try:
                    files = list(result)
                except TypeError:
                    files = [result]

            # ------------------------------------------------
            # Enforce max_files at pipeline level too.
            # ------------------------------------------------

            if max_files is not None:
                try:
                    max_files = int(max_files)

                    if max_files > 0:
                        files = files[:max_files]

                except (TypeError, ValueError):
                    pass

            return files

        except Exception as error:

            print(
                "[Pipeline] File discovery error "
                f"for {folder_path}: {error}"
            )

            return []


    # ========================================================
    # FILE RECORD NORMALIZATION
    # ========================================================

    def normalize_file_record(self, file_record):
        """
        Convert a discovered file record into a dictionary
        suitable for the FileIndex.

        Supports:
            dict
            pathlib.Path
            string path
            objects with path/name attributes
        """

        # ----------------------------------------------------
        # Dictionary
        # ----------------------------------------------------

        if isinstance(file_record, dict):

            record = dict(file_record)

            path = (
                record.get("path")
                or record.get("full_path")
                or record.get("file_path")
            )

            if path:
                path = os.path.abspath(
                    os.path.expanduser(str(path))
                )

                record.setdefault(
                    "path",
                    path,
                )

                record.setdefault(
                    "name",
                    os.path.basename(path),
                )

                record.setdefault(
                    "folder",
                    os.path.dirname(path),
                )

                record.setdefault(
                    "extension",
                    os.path.splitext(path)[1].lower(),
                )

                try:
                    record.setdefault(
                        "size_bytes",
                        os.path.getsize(path),
                    )
                except OSError:
                    record.setdefault(
                        "size_bytes",
                        0,
                    )

                try:
                    record.setdefault(
                        "modified_timestamp",
                        os.path.getmtime(path),
                    )
                except OSError:
                    record.setdefault(
                        "modified_timestamp",
                        0,
                    )

            return record

        # ----------------------------------------------------
        # Path / string
        # ----------------------------------------------------

        if isinstance(
            file_record,
            (str, os.PathLike),
        ):

            path = os.path.abspath(
                os.path.expanduser(
                    os.fspath(file_record)
                )
            )

            return self._build_path_record(path)

        # ----------------------------------------------------
        # Generic object
        # ----------------------------------------------------

        path = getattr(
            file_record,
            "path",
            None,
        )

        if path is None:
            path = getattr(
                file_record,
                "full_path",
                None,
            )

        if path is None:
            path = getattr(
                file_record,
                "file_path",
                None,
            )

        if path:

            path = os.path.abspath(
                os.path.expanduser(str(path))
            )

            record = self._build_path_record(path)

            # Preserve useful attributes when available.

            for attribute in (
                "name",
                "category",
                "type",
                "extension",
                "size_bytes",
                "modified_timestamp",
            ):

                value = getattr(
                    file_record,
                    attribute,
                    None,
                )

                if value is not None:
                    record[attribute] = value

            return record

        return {
            "name": str(file_record),
            "path": str(file_record),
            "discovery_source": "file_discovery",
        }


    # ========================================================
    # PATH RECORD
    # ========================================================

    def _build_path_record(self, path):

        extension = os.path.splitext(
            path
        )[1].lower()

        record = {
            "name": os.path.basename(path),
            "path": path,
            "folder": os.path.dirname(path),
            "extension": extension,
            "discovery_source": "file_discovery",
        }

        try:
            record["size_bytes"] = os.path.getsize(path)
        except OSError:
            record["size_bytes"] = 0

        try:
            record["modified_timestamp"] = (
                os.path.getmtime(path)
            )
        except OSError:
            record["modified_timestamp"] = 0

        # ----------------------------------------------------
        # Category
        # ----------------------------------------------------

        try:

            category_method = getattr(
                self.file_discovery,
                "get_file_category",
                None,
            )

            if category_method is not None:

                category = category_method(
                    path
                )

                if category:
                    record["category"] = category

        except Exception:

            pass

        return record


    # ========================================================
    # INDEX ONE FILE
    # ========================================================

    def index_file(self, file_record):
        """
        Send one normalized file record to FileIndex.

        The method adapts to the existing FileIndex API.
        """

        record = self.normalize_file_record(
            file_record
        )

        # ----------------------------------------------------
        # Try common FileIndex insertion methods.
        # ----------------------------------------------------

        candidate_methods = (
            "index_file",
            "add_file",
            "insert_file",
            "upsert_file",
        )

        for method_name in candidate_methods:

            method = getattr(
                self.file_index,
                method_name,
                None,
            )

            if method is None:
                continue

            try:

                return method(record)

            except TypeError:

                try:
                    return method(
                        record.get("path"),
                        record,
                    )

                except TypeError:
                    continue

        # ----------------------------------------------------
        # If no known API exists, fail clearly.
        # ----------------------------------------------------

        raise AttributeError(
            "FileIndex does not expose a supported "
            "file insertion method. "
            "Expected one of: "
            + ", ".join(candidate_methods)
        )


    # ========================================================
    # INDEX FILE COLLECTION
    # ========================================================

    def index_discovered_files(
        self,
        files,
    ):
        """
        Index a collection of discovered files.
        """

        indexed_count = 0

        for file_record in files:

            try:

                self.index_file(
                    file_record
                )

                indexed_count += 1

            except Exception as error:

                print(
                    "[Pipeline] Index error: "
                    f"{error}"
                )

        return indexed_count


    # ========================================================
    # INDEX ONE FOLDER
    # ========================================================

    def index_folder(
        self,
        folder_path,
        recursive=False,
        max_files=1000,
    ):
        """
        Discover and index files from one folder.
        """

        folder_path = os.path.abspath(
            os.path.expanduser(
                str(folder_path)
            )
        )

        print()
        print("------------------------------------------")
        print("[Pipeline] Indexing folder:")
        print(folder_path)

        start_time = time.time()

        # ----------------------------------------------------
        # DISCOVERY
        # ----------------------------------------------------

        files = self.discover_files(
            folder_path=folder_path,
            recursive=recursive,
            max_files=max_files,
        )

        discovered_count = len(files)

        print(
            f"[Pipeline] Files discovered : "
            f"{discovered_count}"
        )

        # ----------------------------------------------------
        # INDEXING
        # ----------------------------------------------------

        indexed_count = self.index_discovered_files(
            files
        )

        elapsed = time.time() - start_time

        print(
            f"[Pipeline] Files indexed    : "
            f"{indexed_count}"
        )

        print(
            f"[Pipeline] Time              : "
            f"{elapsed:.2f} sec"
        )

        # ----------------------------------------------------
        # REAL SUCCESS CONDITION
        # ----------------------------------------------------

        success = (
            discovered_count > 0
            and indexed_count > 0
        )

        return {
            "folder": folder_path,
            "discovered": discovered_count,
            "indexed": indexed_count,
            "success": success,
            "elapsed_seconds": elapsed,
        }


    # ========================================================
    # DATABASE COUNT
    # ========================================================

    def get_index_count(self):
        """
        Get total number of indexed records when the
        FileIndex exposes a count method.
        """

        candidate_methods = (
            "count",
            "count_files",
            "get_count",
            "total_files",
        )

        for method_name in candidate_methods:

            method = getattr(
                self.file_index,
                method_name,
                None,
            )

            if method is None:
                continue

            try:

                value = method()

                if isinstance(value, int):
                    return value

                return int(value)

            except Exception:
                continue

        return None


# ============================================================
# STEP 9.5 TEST
# ============================================================

def run_step_9_5_test():

    print()
    print("==========================================")
    print("      MYX STEP 9.5 PIPELINE TEST")
    print("==========================================")

    pipeline = IndexingPipeline()

    # --------------------------------------------------------
    # Controlled test folder.
    #
    # We intentionally test only src\system here.
    # Do NOT scan the entire C:\ drive yet.
    # --------------------------------------------------------

    test_folder = os.path.join(
        PROJECT_ROOT,
        "src",
        "system",
    )

    print()
    print("Test folder:")
    print(test_folder)

    if not os.path.isdir(test_folder):

        print()
        print("PIPELINE TEST FAILED")
        print(
            "Test folder does not exist:"
        )
        print(test_folder)

        return False

    # --------------------------------------------------------
    # Run pipeline.
    # --------------------------------------------------------

    result = pipeline.index_folder(
        folder_path=test_folder,
        recursive=False,
        max_files=20,
    )

    print()
    print("Pipeline result:")
    print(
        f"Folder     : {result['folder']}"
    )
    print(
        f"Discovered : {result['discovered']}"
    )
    print(
        f"Indexed    : {result['indexed']}"
    )
    print(
        f"Success    : {result['success']}"
    )

    # --------------------------------------------------------
    # Database verification.
    # --------------------------------------------------------

    database_count = pipeline.get_index_count()

    print()
    print(
        f"Database records: "
        f"{database_count}"
    )

    # --------------------------------------------------------
    # REAL TEST CONDITIONS
    # --------------------------------------------------------

    if result["discovered"] <= 0:

        print()
        print(
            "PIPELINE TEST FAILED"
        )

        print(
            "Reason: FileDiscovery returned "
            "zero files."
        )

        return False

    if result["indexed"] <= 0:

        print()
        print(
            "PIPELINE TEST FAILED"
        )

        print(
            "Reason: Files were discovered "
            "but none were indexed."
        )

        return False

    if database_count is not None:

        if database_count <= 0:

            print()
            print(
                "PIPELINE TEST FAILED"
            )

            print(
                "Reason: FileIndex contains "
                "zero records."
            )

            return False

    print()
    print(
        "FILE INDEXING PIPELINE TEST: PASS"
    )

    print()
    print(
        "=========================================="
    )
    print(
        "       STEP 9.5 TEST PASSED"
    )
    print(
        "=========================================="
    )

    return True


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    success = run_step_9_5_test()

    if not success:
        sys.exit(1)

    sys.exit(0)
    

