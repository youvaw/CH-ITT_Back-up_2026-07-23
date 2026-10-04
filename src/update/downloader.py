"""
=========================================
CHITT - Downloader
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import hashlib
import os
from pathlib import Path

import requests


class Downloader:

    def __init__(self):

        self.download_directory = Path(
            "downloads"
        )

        self.download_directory.mkdir(

            parents=True,

            exist_ok=True

        )

    # ---------------------------------
    # Download File
    # ---------------------------------

    def download(

        self,

        url,

        filename=None

    ):

        try:

            if filename is None:

                filename = url.split("/")[-1]

            destination = (

                self.download_directory / filename

            )

            response = requests.get(

                url,

                stream=True,

                timeout=30

            )

            response.raise_for_status()

            with open(

                destination,

                "wb"

            ) as file:

                for chunk in response.iter_content(

                    chunk_size=8192

                ):

                    if chunk:

                        file.write(chunk)

            return {

                "success": True,

                "file": str(destination)

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # SHA256 Checksum
    # ---------------------------------

    def checksum(self, file_path):

        sha = hashlib.sha256()

        with open(file_path, "rb") as file:

            for chunk in iter(

                lambda: file.read(4096),

                b""

            ):

                sha.update(chunk)

        return sha.hexdigest()

    # ---------------------------------
    # Verify Checksum
    # ---------------------------------

    def verify(

        self,

        file_path,

        expected_hash

    ):

        return (

            self.checksum(file_path)

            == expected_hash

        )

    # ---------------------------------
    # File Exists
    # ---------------------------------

    def exists(self, filename):

        return (

            self.download_directory /

            filename

        ).exists()

    # ---------------------------------
    # Delete File
    # ---------------------------------

    def delete(self, filename):

        file_path = (

            self.download_directory /

            filename

        )

        if file_path.exists():

            os.remove(file_path)

            return True

        return False

    # ---------------------------------
    # List Downloads
    # ---------------------------------

    def list(self):

        return [

            file.name

            for file in

            self.download_directory.iterdir()

            if file.is_file()

        ]

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "Downloader",

            "directory": str(

                self.download_directory

            ),

            "downloads": len(

                self.list()

            ),

            "status": "OK"

        }


if __name__ == "__main__":

    downloader = Downloader()

    print(

        downloader.health()

    )
    
