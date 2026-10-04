"""
=========================================
CHITT - Authorization
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class Authorization:

    def __init__(self):

        self.roles = {

            "admin": {

                "all"

            },

            "user": {

                "read",

                "write",

                "automation",

                "vision",

                "voice"

            },

            "guest": {

                "read"

            }

        }

        self.user_roles = {}

    # ---------------------------------
    # Assign Role
    # ---------------------------------

    def assign_role(

        self,

        username,

        role

    ):

        if role not in self.roles:

            return {

                "success": False,

                "message": "Invalid role."

            }

        self.user_roles[username] = role

        return {

            "success": True

        }

    # ---------------------------------
    # Get Role
    # ---------------------------------

    def role(self, username):

        return self.user_roles.get(

            username,

            "guest"

        )

    # ---------------------------------
    # Check Permission
    # ---------------------------------

    def check(

        self,

        username,

        permission

    ):

        role = self.role(username)

        permissions = self.roles.get(role, set())

        if "all" in permissions:

            return True

        return permission in permissions

    # ---------------------------------
    # Add Permission
    # ---------------------------------

    def add_permission(

        self,

        role,

        permission

    ):

        if role not in self.roles:

            self.roles[role] = set()

        self.roles[role].add(permission)

        return True

    # ---------------------------------
    # Remove Permission
    # ---------------------------------

    def remove_permission(

        self,

        role,

        permission

    ):

        if role in self.roles:

            self.roles[role].discard(permission)

        return True

    # ---------------------------------
    # List Roles
    # ---------------------------------

    def list_roles(self):

        return list(self.roles.keys())

    # ---------------------------------
    # Permissions
    # ---------------------------------

    def permissions(

        self,

        role

    ):

        return list(

            self.roles.get(

                role,

                set()

            )

        )

    # ---------------------------------
    # User Information
    # ---------------------------------

    def user_info(

        self,

        username

    ):

        role = self.role(username)

        return {

            "username": username,

            "role": role,

            "permissions":

                self.permissions(role)

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "Authorization",

            "roles": len(self.roles),

            "status": "OK"

        }


if __name__ == "__main__":

    auth = Authorization()

    auth.assign_role(

        "admin",

        "admin"

    )

    print(

        auth.user_info("admin")

    )

    print(

        auth.health()

    )
    
