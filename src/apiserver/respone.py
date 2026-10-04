"""
=========================================
CHITT - API Response
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

from datetime import datetime


class APIResponse:

    # ---------------------------------
    # Success Response
    # ---------------------------------

    @staticmethod
    def success(

        message="Success",

        data=None

    ):

        return {

            "success": True,

            "message": message,

            "data": data,

            "timestamp": datetime.now().isoformat()

        }

    # ---------------------------------
    # Error Response
    # ---------------------------------

    @staticmethod
    def error(

        message="Error",

        code=500

    ):

        return {

            "success": False,

            "code": code,

            "message": message,

            "timestamp": datetime.now().isoformat()

        }

    # ---------------------------------
    # Validation Error
    # ---------------------------------

    @staticmethod
    def validation_error(

        errors

    ):

        return {

            "success": False,

            "code": 400,

            "message": "Validation Failed",

            "errors": errors,

            "timestamp": datetime.now().isoformat()

        }

    # ---------------------------------
    # Not Found
    # ---------------------------------

    @staticmethod
    def not_found(

        resource="Resource"

    ):

        return {

            "success": False,

            "code": 404,

            "message": f"{resource} not found",

            "timestamp": datetime.now().isoformat()

        }

    # ---------------------------------
    # Unauthorized
    # ---------------------------------

    @staticmethod
    def unauthorized():

        return {

            "success": False,

            "code": 401,

            "message": "Unauthorized",

            "timestamp": datetime.now().isoformat()

        }

    # ---------------------------------
    # Forbidden
    # ---------------------------------

    @staticmethod
    def forbidden():

        return {

            "success": False,

            "code": 403,

            "message": "Forbidden",

            "timestamp": datetime.now().isoformat()

        }

    # ---------------------------------
    # Pagination Response
    # ---------------------------------

    @staticmethod
    def paginated(

        items,

        page,

        page_size,

        total

    ):

        return {

            "success": True,

            "page": page,

            "page_size": page_size,

            "total": total,

            "data": items,

            "timestamp": datetime.now().isoformat()

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    @staticmethod
    def health():

        return {

            "module": "APIResponse",

            "status": "OK"

        }


if __name__ == "__main__":

    print(

        APIResponse.success(

            "Server Running"

        )

    )

    print(APIResponse.health())
    
