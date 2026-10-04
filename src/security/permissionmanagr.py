"""
=========================================
CHITT - Permission Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class PermissionManager:

    def __init__(self):

        self.permissions = {

            "camera": False,
            "microphone": False,
            "filesystem": False,
            "automation": False,
            "internet": False,
            "clipboard": False,
            "notifications": False,
            "location": False

        }

    # ---------------------------------
    # Grant Permission
    # ---------------------------------

    def grant(self, permission):

        if permission in self.permissions:

            self.permissions[permission] = True

            return True

        return False

    # ---------------------------------
    # Revoke Permission
    # ---------------------------------

    def revoke(self, permission):

        if permission in self.permissions:

            self.permissions[permission] = False

            return True

        return False

    # ---------------------------------
    # Check Permission
    # ---------------------------------

    def check(self, permission):

        return self.permissions.get(

            permission,

            False

        )

    # ---------------------------------
    # Toggle Permission
    # ---------------------------------

    def toggle(self, permission):

        if permission in self.permissions:

            self.permissions[permission] = (

                not self.permissions[permission]

            )

            return self.permissions[permission]

        return False

    # ---------------------------------
    # Grant All
    # ---------------------------------

    def grant_all(self):

        for permission in self.permissions:

            self.permissions[permission] = True

    # ---------------------------------
    # Revoke All
    # ---------------------------------

    def revoke_all(self):

        for permission in self.permissions:

            self.permissions[permission] = False

    # ---------------------------------
    # List Permissions
    # ---------------------------------

    def list_permissions(self):

        return self.permissions

    # ---------------------------------
    # Enabled Permissions
    # ---------------------------------

    def enabled(self):

        return [

            name

            for name, value

            in self.permissions.items()

            if value

        ]

    # ---------------------------------
    # Disabled Permissions
    # ---------------------------------

    def disabled(self):

        return [

            name

            for name, value

            in self.permissions.items()

            if not value

        ]

    # ---------------------------------
    # Reset
    # ---------------------------------

    def reset(self):

        self.revoke_all()

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "PermissionManager",

            "enabled": len(self.enabled()),

            "status": "OK"

        }


if __name__ == "__main__":

    manager = PermissionManager()

    manager.grant("camera")

    manager.grant("microphone")

    print(manager.list_permissions())

    print(manager.health())
    
