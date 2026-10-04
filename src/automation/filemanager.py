"""
=========================================
CHITT - File Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import os
import shutil
from pathlib import Path


class FileManager:

    def __init__(self):

        self.encoding = "utf-8"

    # ---------------------------------
    # Create File
    # ---------------------------------

    def create(self, path):

        try:

            Path(path).parent.mkdir(

                parents=True,

                exist_ok=True

            )

            Path(path).touch(

                exist_ok=True

            )

            return {

                "success": True,

                "path": path

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Read File
    # ---------------------------------

    def read(self, path):

        try:

            with open(

                path,

                "r",

                encoding=self.encoding

            ) as file:

                return {

                    "success": True,

                    "content": file.read()

                }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Write File
    # ---------------------------------

    def write(self, path, content):

        try:

            with open(

                path,

                "w",

                encoding=self.encoding

            ) as file:

                file.write(content)

            return {

                "success": True

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Append File
    # ---------------------------------

    def append(self, path, content):

        try:

            with open(

                path,

                "a",

                encoding=self.encoding

            ) as file:

                file.write(content)

            return {

                "success": True

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Copy File
    # ---------------------------------

    def copy(self, source, destination):

        try:

            shutil.copy2(

                source,

                destination

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
    # Move File
    # ---------------------------------

    def move(self, source, destination):

        try:

            shutil.move(

                source,

                destination

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
    # Rename File
    # ---------------------------------

    def rename(self, source, destination):

        try:

            os.rename(

                source,

                destination

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
    # Delete File
    # ---------------------------------

    def delete(self, path):

        try:

            os.remove(path)

            return {

                "success": True

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

        return os.path.exists(path)

    # ---------------------------------
    # File Size
    # ---------------------------------

    def size(self, path):

        try:

            return {

                "success": True,

                "size": os.path.getsize(path)

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(self, command, *args):

        command = command.lower()

        if hasattr(self, command):

            return getattr(self, command)(*args)

        return {

            "success": False,

            "message": "Unknown command."

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "FileManager",

            "encoding": self.encoding,

            "status": "OK"

        }


if __name__ == "__main__":

    manager = FileManager()

    manager.create("demo.txt")

    manager.write(

        "demo.txt",

        "Hello CHITT"

    )

    print(

        manager.read("demo.txt")

    )

    print(

        manager.health()

    )
    
