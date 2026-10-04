"""
=========================================
CHITT - Calculator Plugin
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import math
import operator

from plugins.plugin_base import PluginBase


class CalculatorPlugin(PluginBase):

    def __init__(self):

        super().__init__()

        self.name = "CalculatorPlugin"

        self.version = "1.0.0"

        self.description = "Mathematical Calculator Plugin"

        self.operations = {

            "+": operator.add,

            "-": operator.sub,

            "*": operator.mul,

            "/": operator.truediv,

            "%": operator.mod,

            "**": operator.pow

        }

    # ---------------------------------
    # Startup
    # ---------------------------------

    def start(self):

        print(f"{self.name} Started")

    # ---------------------------------
    # Shutdown
    # ---------------------------------

    def stop(self):

        print(f"{self.name} Stopped")

    # ---------------------------------
    # Safe Evaluate
    # ---------------------------------

    def calculate(self, expression):

        allowed = {

            "__builtins__": {},

            "abs": abs,

            "round": round,

            "min": min,

            "max": max,

            "pow": pow,

            "sqrt": math.sqrt,

            "sin": math.sin,

            "cos": math.cos,

            "tan": math.tan,

            "pi": math.pi,

            "e": math.e,

            "log": math.log,

            "log10": math.log10,

            "factorial": math.factorial,

            "ceil": math.ceil,

            "floor": math.floor

        }

        try:

            result = eval(

                expression,

                allowed,

                {}

            )

            return {

                "success": True,

                "expression": expression,

                "result": result

            }

        except Exception as error:

            return {

                "success": False,

                "expression": expression,

                "error": str(error)

            }

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(

        self,

        expression

    ):

        return self.calculate(expression)

    # ---------------------------------
    # Settings
    # ---------------------------------

    def settings(self):

        return {

            "scientific": True,

            "precision": 10

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "plugin": self.name,

            "enabled": self.enabled,

            "scientific": True,

            "status": "OK"

        }


if __name__ == "__main__":

    calc = CalculatorPlugin()

    calc.start()

    print(calc.execute("5+8"))

    print(calc.execute("sqrt(144)"))

    print(calc.execute("sin(pi/2)"))

    calc.stop()
    
