import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class FileDiscovery:
    """
    MYX File Discovery

    Discovers files inside a supplied folder.

    Default behavior:
    - current folder only
    - no recursive drive scan
    - read-only
    """

    def __init__(self):
        print("[FileDiscovery] Initialized")

    def get_file_category(self, extension):
        extension = extension.lower()

        categories = {
            "document": {
                ".doc", ".docx", ".txt", ".rtf", ".odt"
            },
            "pdf": {
                ".pdf"
            },
            "spreadsheet": {
                ".xls", ".xlsx", ".csv", ".ods"
            },
            "presentation": {
                ".ppt", ".pptx", ".odp"
            },
            "image": {
                ".jpg", ".jpeg", ".png", ".gif",
                ".bmp", ".webp", ".svg", ".ico"
            },
            "audio": {
                ".mp3", ".wav", ".flac", ".aac",
                ".m4a", ".ogg"
            },
            "video": {
                ".mp4", ".mkv", ".avi", ".mov",
                ".wmv", ".webm"
            },
            "archive": {
                ".zip", ".rar", ".7z", ".tar", ".gz"
            },
            "code": {
                ".py", ".pyw", ".c", ".cpp", ".h",
                ".hpp", ".java", ".js", ".jsx",
                ".ts", ".tsx", ".html", ".css",
                ".json", ".xml", ".sql", ".sh",
                ".bat", ".ps1"
            },
        }

        for category, extensions in categories.items():
            if extension in extensions:
                return category

        return "other"

    def discover_folder(
        self,
        folder_path,
        recursive=False,
        max_files=None,
    ):
        """
        Discover files inside one folder.

        recursive=False:
            only current folder.

        recursive=True:
            includes subfolders.
        """

        folder_path = os.path.normpath(
            str(folder_path).strip()
        )

        if not os.path.isdir(folder_path):
            return []

        results = []

        if recursive:
            walker = os.walk(folder_path)
        else:
            try:
                entries = os.scandir(folder_path)
            except (PermissionError, OSError):
                return []

            walker = [
                (
                    folder_path,
                    [],
                    [
                        entry.name
                        for entry in entries
                        if entry.is_file()
                    ],
                )
            ]

        for root, _, filenames in walker:

            for filename in filenames:

                if max_files is not None:
                    if len(results) >= max_files:
                        return results

                full_path = os.path.join(
                    root,
                    filename
                )

                try:
                    stat = os.stat(full_path)

                    extension = os.path.splitext(
                        filename
                    )[1].lower()

                    results.append({
                        "name": filename,
                        "path": os.path.normpath(full_path),
                        "folder": os.path.normpath(root),
                        "extension": extension,
                        "category": self.get_file_category(
                            extension
                        ),
                        "size_bytes": stat.st_size,
                        "modified_timestamp": stat.st_mtime,
                        "type": "file",
                        "discovery_source": "filesystem",
                    })

                except (PermissionError, OSError):
                    continue

        return results


def run_test():

    print("\n==========================================")
    print("         MYX FILE DISCOVERY TEST")
    print("==========================================")

    discovery = FileDiscovery()

    test_folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    print(f"\nTest folder:")
    print(test_folder)

    files = discovery.discover_folder(
        test_folder,
        recursive=False,
        max_files=20,
    )

    print(f"\nFiles discovered: {len(files)}")

    assert isinstance(files, list)

    for item in files[:20]:

        print("\n------------------------------------------")
        print(f"Name      : {item['name']}")
        print(f"Extension : {item['extension']}")
        print(f"Category  : {item['category']}")
        print(f"Size      : {item['size_bytes']} bytes")
        print(f"Path      : {item['path']}")

    print("\n==========================================")
    print("FILE DISCOVERY TEST PASSED")
    print("==========================================")


if __name__ == "__main__":
    run_test()
    
