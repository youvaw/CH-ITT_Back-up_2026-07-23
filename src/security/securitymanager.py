"""
=========================================
CHITT - Security Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from security.authentication import Authentication
from security.authorization import Authorization
from security.encryption import Encryption
from security.password_manager import PasswordManager
from security.permission_manager import PermissionManager
from security.secure_storage import SecureStorage
from security.audit_logger import AuditLogger


class SecurityManager:

    def __init__(self):

        self.authentication = Authentication()

        self.authorization = Authorization()

        self.encryption = Encryption()

        self.passwords = PasswordManager()

        self.permissions = PermissionManager()

        self.storage = SecureStorage()

        self.audit = AuditLogger()

        self.active = False

    # ---------------------------------
    # Start
    # ---------------------------------

    def start(self):

        self.active = True

        self.audit.log(

            "Security Started"

        )

        return True

    # ---------------------------------
    # Stop
    # ---------------------------------

    def stop(self):

        self.active = False

        self.audit.log(

            "Security Stopped"

        )

        return True

    # ---------------------------------
    # Encrypt
    # ---------------------------------

    def encrypt(self, data):

        return self.encryption.encrypt(data)

    # ---------------------------------
    # Decrypt
    # ---------------------------------

    def decrypt(self, data):

        return self.encryption.decrypt(data)

    # ---------------------------------
    # Login
    # ---------------------------------

    def login(

        self,

        username,

        password

    ):

        result = self.authentication.login(

            username,

            password

        )

        self.audit.log(

            f"Login : {username}"

        )

        return result

    # ---------------------------------
    # Logout
    # ---------------------------------

    def logout(self):

        self.authentication.logout()

        self.audit.log("Logout")

    # ---------------------------------
    # Permission
    # ---------------------------------

    def check_permission(

        self,

        permission

    ):

        return self.permissions.check(

            permission

        )

    # ---------------------------------
    # Store Secret
    # ---------------------------------

    def save(

        self,

        key,

        value

    ):

        return self.storage.save(

            key,

            value

        )

    # ---------------------------------
    # Read Secret
    # ---------------------------------

    def load(self, key):

        return self.storage.load(key)

    # ---------------------------------
    # Status
    # ---------------------------------

    def status(self):

        return {

            "active": self.active,

            "authenticated":

            self.authentication.is_authenticated()

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "SecurityManager",

            "status": "OK",

            "active": self.active

        }


if __name__ == "__main__":

    manager = SecurityManager()

    manager.start()

    print(manager.health())
    
