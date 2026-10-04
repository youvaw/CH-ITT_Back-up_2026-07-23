# ============================================================
# MYX - FOLDER DISCOVERY
# User / Windows Important Folder Locations
# ============================================================

import os


class FolderDiscovery:
    """
    MYX Folder / Location Discovery

    Discovers important user/system locations.
    Supports normal Windows folders and OneDrive folders.
    Does NOT recursively scan drives.
    """

    def __init__(self):
        print("[FolderDiscovery] Initialized")

    # ========================================================
    # GET IMPORTANT LOCATIONS
    # ========================================================

    def get_locations(self):

        user_profile = os.environ.get(
            "USERPROFILE",
            os.path.expanduser("~")
        )

        onedrive = os.path.join(
            user_profile,
            "OneDrive"
        )

        # ----------------------------------------------------
        # Desktop
        # ----------------------------------------------------

        desktop_path = os.path.join(
            user_profile,
            "Desktop"
        )

        # If normal Desktop does not exist,
        # use OneDrive Desktop.
        if not os.path.isdir(desktop_path):

            onedrive_desktop = os.path.join(
                onedrive,
                "Desktop"
            )

            if os.path.isdir(onedrive_desktop):
                desktop_path = onedrive_desktop

        # ----------------------------------------------------
        # Documents
        # ----------------------------------------------------

        documents_path = os.path.join(
            user_profile,
            "Documents"
        )

        if not os.path.isdir(documents_path):

            onedrive_documents = os.path.join(
                onedrive,
                "Documents"
            )

            if os.path.isdir(onedrive_documents):
                documents_path = onedrive_documents

        # ----------------------------------------------------
        # Pictures
        # ----------------------------------------------------

        pictures_path = os.path.join(
            user_profile,
            "Pictures"
        )

        if not os.path.isdir(pictures_path):

            onedrive_pictures = os.path.join(
                onedrive,
                "Pictures"
            )

            if os.path.isdir(onedrive_pictures):
                pictures_path = onedrive_pictures

        # ----------------------------------------------------
        # Music
        # ----------------------------------------------------

        music_path = os.path.join(
            user_profile,
            "Music"
        )

        if not os.path.isdir(music_path):

            onedrive_music = os.path.join(
                onedrive,
                "Music"
            )

            if os.path.isdir(onedrive_music):
                music_path = onedrive_music

        # ----------------------------------------------------
        # Videos
        # ----------------------------------------------------

        videos_path = os.path.join(
            user_profile,
            "Videos"
        )

        if not os.path.isdir(videos_path):

            onedrive_videos = os.path.join(
                onedrive,
                "Videos"
            )

            if os.path.isdir(onedrive_videos):
                videos_path = onedrive_videos

        # ----------------------------------------------------
        # Final locations
        # ----------------------------------------------------

        locations = {

            "user_home": user_profile,

            "desktop": desktop_path,

            "documents": documents_path,

            "downloads": os.path.join(
                user_profile,
                "Downloads"
            ),

            "pictures": pictures_path,

            "music": music_path,

            "videos": videos_path,

            "onedrive": onedrive,
        }

        # ----------------------------------------------------
        # Convert to discovery records
        # ----------------------------------------------------

        results = []

        for name, path in locations.items():

            path = os.path.normpath(path)

            results.append(
                {
                    "name": name,
                    "path": path,
                    "exists": os.path.isdir(path),
                    "type": "folder",
                    "discovery_source": (
                        "windows_user_profile"
                    ),
                }
            )

        return results

    # ========================================================
    # TEST
    # ========================================================

    def run_test(self):

        print("=" * 65)
        print("        MYX FOLDER DISCOVERY TEST")
        print("=" * 65)

        locations = self.get_locations()

        print(
            f"\nLocations discovered: {len(locations)}"
        )

        passed = 0

        # ----------------------------------------------------
        # Test 1
        # ----------------------------------------------------

        print("\n[TEST 1] User Home")

        user_home = next(
            (
                item
                for item in locations
                if item["name"] == "user_home"
            ),
            None
        )

        if user_home and user_home["exists"]:
            print(
                f"User Home: {user_home['path']}"
            )
            print("USER HOME TEST: PASS")
            passed += 1
        else:
            print("USER HOME TEST: FAIL")

        # ----------------------------------------------------
        # Test 2
        # ----------------------------------------------------

        print("\n[TEST 2] Desktop")

        desktop = next(
            (
                item
                for item in locations
                if item["name"] == "desktop"
            ),
            None
        )

        if desktop and desktop["exists"]:
            print(
                f"Desktop: {desktop['path']}"
            )
            print("DESKTOP TEST: PASS")
            passed += 1
        else:
            print("DESKTOP TEST: FAIL")

        # ----------------------------------------------------
        # Test 3
        # ----------------------------------------------------

        print("\n[TEST 3] OneDrive")

        onedrive_item = next(
            (
                item
                for item in locations
                if item["name"] == "onedrive"
            ),
            None
        )

        if onedrive_item and onedrive_item["exists"]:
            print(
                f"OneDrive: {onedrive_item['path']}"
            )
            print("ONEDRIVE TEST: PASS")
            passed += 1
        else:
            print("ONEDRIVE TEST: FAIL")

        # ----------------------------------------------------
        # Test 4
        # ----------------------------------------------------

        print("\n[TEST 4] Existing Folders")

        existing = [
            item
            for item in locations
            if item["exists"]
        ]

        print(
            f"Existing folders: {len(existing)}"
        )

        if existing:
            print("EXISTING FOLDERS TEST: PASS")
            passed += 1
        else:
            print("EXISTING FOLDERS TEST: FAIL")

        # ----------------------------------------------------
        # Test 5
        # ----------------------------------------------------

        print("\n[TEST 5] Folder Metadata")

        valid_metadata = all(
            isinstance(item, dict)
            and item.get("name")
            and item.get("path")
            and item.get("type") == "folder"
            for item in locations
        )

        if valid_metadata:
            print("METADATA TEST: PASS")
            passed += 1
        else:
            print("METADATA TEST: FAIL")

        # ----------------------------------------------------
        # Final result
        # ----------------------------------------------------

        print("\n" + "-" * 65)

        print(
            f"Tests passed : {passed}/5"
        )

        if passed == 5:

            print(
                "FOLDER DISCOVERY TEST: PASS"
            )

            return True

        print(
            "FOLDER DISCOVERY TEST: FAIL"
        )

        return False


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    discovery = FolderDiscovery()

    success = discovery.run_test()

    raise SystemExit(
        0 if success else 1
    )
