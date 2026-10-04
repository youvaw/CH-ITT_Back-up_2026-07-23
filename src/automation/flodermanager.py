"""
=========================================
CHITT - Folder Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import shutil
from pathlib import Path


class FolderManager:

    def __init__(self):

        self.home = str(Path.home())

    # ---------------------------------
    # Create Folder
    # ---------------------------------

    def create(self, path):

        try:

            os.makedirs(path, exist_ok=True)

            return {

                "success": True,

                "folder": path

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Delete Folder
    # ---------------------------------

    def delete(self, path):

        try:

            shutil.rmtree(path)

            return {

                "success": True

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Rename Folder
    # ---------------------------------

    def rename(self, source, destination):

        try:

            os.rename(source, destination)

            return {

                "success": True

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Copy Folder
    # ---------------------------------

    def copy(self, source, destination):

        try:

            shutil.copytree(

                source,

                destination,

                dirs_exist_ok=True

            )

            return {

                "success": True

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Move Folder
    # ---------------------------------

    def move(self, source, destination):

        try:

            shutil.move(source, destination)

            return {

                "success": True

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # List Folder
    # ---------------------------------

    def list(self, path):

        try:

            return {

                "success": True,

                "items": os.listdir(path)

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Exists
    # ---------------------------------

    def exists(self, path):

        return os.path.isdir(path)

    # ---------------------------------
    # Search Folder
    # ---------------------------------

    def search(self, root, keyword):

        results = []

        try:

            for folder, dirs, files in os.walk(root):

                for item in dirs:

                    if keyword.lower() in item.lower():

                        results.append(

                            os.path.join(folder, item)

                        )

            return {

                "success": True,

                "results": results

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Folder Size
    # ---------------------------------

    def size(self, path):

        total = 0

        try:

            for folder, dirs, files in os.walk(path):

                for file in files:

                    file_path = os.path.join(folder, file)

                    total += os.path.getsize(file_path)

            return {

                "success": True,

                "size": total

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "FolderManager",

            "home": self.home,

            "status": "OK"

        }


if __name__ == "__main__":

    manager = FolderManager()

    print(manager.health())
    
