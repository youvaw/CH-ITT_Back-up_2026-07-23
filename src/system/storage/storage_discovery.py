import os
import sys
import shutil
import ctypes
import string

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class StorageDiscovery:
    """
    MYX Storage Discovery

    Step 9.1:
    Discover available Windows storage drives.

    This module is READ-ONLY.
    It does not scan files or modify storage.
    """

    def __init__(self):
        print("[StorageDiscovery] Initialized")

    def get_drive_letters(self):
        """
        Return available Windows drive letters.
        """

        drives = []

        try:
            bitmask = ctypes.windll.kernel32.GetLogicalDrives()

            for index, letter in enumerate(string.ascii_uppercase):
                if bitmask & (1 << index):
                    drives.append(f"{letter}:\\")

        except Exception as e:
            print(f"[StorageDiscovery] Drive detection warning: {e}")

            # Safe fallback
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"

                if os.path.exists(drive):
                    drives.append(drive)

        return drives

    def get_drive_type(self, drive):
        """
        Identify basic Windows drive type.
        """

        DRIVE_TYPES = {
            0: "unknown",
            1: "no_root_directory",
            2: "removable",
            3: "fixed",
            4: "network",
            5: "cdrom",
            6: "ramdisk",
        }

        try:
            drive_type = ctypes.windll.kernel32.GetDriveTypeW(
                ctypes.c_wchar_p(drive)
            )

            return DRIVE_TYPES.get(
                drive_type,
                "unknown"
            )

        except Exception:
            return "unknown"

    def get_filesystem(self, drive):
        """
        Get filesystem name such as NTFS/exFAT/FAT32.
        """

        try:
            volume_name_buffer = ctypes.create_unicode_buffer(261)
            filesystem_buffer = ctypes.create_unicode_buffer(261)

            serial_number = ctypes.c_ulong()
            max_component_length = ctypes.c_ulong()
            filesystem_flags = ctypes.c_ulong()

            result = ctypes.windll.kernel32.GetVolumeInformationW(
                ctypes.c_wchar_p(drive),
                volume_name_buffer,
                len(volume_name_buffer),
                ctypes.byref(serial_number),
                ctypes.byref(max_component_length),
                ctypes.byref(filesystem_flags),
                filesystem_buffer,
                len(filesystem_buffer),
            )

            if result:
                return filesystem_buffer.value or "unknown"

        except Exception:
            pass

        return "unknown"

    def get_space(self, drive):
        """
        Return total, used and free storage in bytes.
        """

        try:
            total, used, free = shutil.disk_usage(drive)

            return {
                "total_bytes": total,
                "used_bytes": used,
                "free_bytes": free,
            }

        except Exception as e:
            return {
                "total_bytes": None,
                "used_bytes": None,
                "free_bytes": None,
                "error": str(e),
            }

    def discover_drive(self, drive):
        """
        Build one normalized drive record.
        """

        drive = str(drive).strip()

        space = self.get_space(drive)

        return {
            "drive": drive,
            "drive_type": self.get_drive_type(drive),
            "filesystem": self.get_filesystem(drive),
            "total_bytes": space.get("total_bytes"),
            "used_bytes": space.get("used_bytes"),
            "free_bytes": space.get("free_bytes"),
            "read_only": False,
            "discovery_source": "windows",
        }

    def discover(self):
        """
        Discover all currently available drives.
        """

        drives = self.get_drive_letters()

        results = []

        for drive in drives:
            try:
                results.append(
                    self.discover_drive(drive)
                )
            except Exception as e:
                print(
                    f"[StorageDiscovery] "
                    f"Unable to inspect {drive}: {e}"
                )

        return results


def format_gb(value):
    """
    Convert bytes to GB for display only.
    """

    if value is None:
        return "N/A"

    return f"{value / (1024 ** 3):.2f} GB"


def run_test():

    print("\n==========================================")
    print("       MYX STORAGE DISCOVERY TEST")
    print("==========================================")

    discovery = StorageDiscovery()

    drives = discovery.discover()

    print(f"\nDrives discovered: {len(drives)}")

    assert isinstance(drives, list)

    for item in drives:

        print("\n------------------------------------------")
        print(f"Drive       : {item['drive']}")
        print(f"Type        : {item['drive_type']}")
        print(f"Filesystem  : {item['filesystem']}")
        print(f"Total       : {format_gb(item['total_bytes'])}")
        print(f"Used        : {format_gb(item['used_bytes'])}")
        print(f"Free        : {format_gb(item['free_bytes'])}")
        print(f"Read Only   : {item['read_only']}")
        print(f"Source      : {item['discovery_source']}")

    print("\n==========================================")

    if drives:
        print("STORAGE DISCOVERY TEST PASSED")
    else:
        print("STORAGE DISCOVERY TEST FAILED")
        raise RuntimeError(
            "No Windows drives were discovered."
        )

    print("==========================================")


if __name__ == "__main__":
    run_test()
    
