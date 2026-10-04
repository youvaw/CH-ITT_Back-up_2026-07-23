"""
=========================================
CHITT - Workflow Engine
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import time


class Workflow:

    def __init__(self):

        self.steps = []

        self.name = "Workflow"

        self.running = False

        self.current_step = 0

    # ---------------------------------
    # Set Name
    # ---------------------------------

    def set_name(self, name):

        self.name = name

    # ---------------------------------
    # Add Step
    # ---------------------------------

    def add_step(

        self,

        action,

        parameters=None

    ):

        if parameters is None:

            parameters = {}

        self.steps.append({

            "action": action,

            "parameters": parameters

        })

    # ---------------------------------
    # Remove Step
    # ---------------------------------

    def remove_step(self, index):

        if 0 <= index < len(self.steps):

            del self.steps[index]

            return True

        return False

    # ---------------------------------
    # Clear
    # ---------------------------------

    def clear(self):

        self.steps.clear()

        self.current_step = 0

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(self, workflow=None):

        if workflow:

            self.steps = workflow

        self.running = True

        results = []

        for index, step in enumerate(self.steps):

            self.current_step = index + 1

            try:

                print(

                    f"[{self.current_step}] "

                    f"{step['action']}"

                )

                time.sleep(0.2)

                results.append({

                    "step": self.current_step,

                    "action": step["action"],

                    "success": True

                })

            except Exception as error:

                results.append({

                    "step": self.current_step,

                    "action": step["action"],

                    "success": False,

                    "error": str(error)

                })

                break

        self.running = False

        return results

    # ---------------------------------
    # Status
    # ---------------------------------

    def status(self):

        return {

            "name": self.name,

            "running": self.running,

            "steps": len(self.steps),

            "current_step": self.current_step

        }

    # ---------------------------------
    # Information
    # ---------------------------------

    def info(self):

        return {

            "workflow": self.name,

            "steps": self.steps

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "Workflow",

            "status": "OK",

            "running": self.running

        }


if __name__ == "__main__":

    wf = Workflow()

    wf.set_name("Open VS Code Project")

    wf.add_step("Launch VS Code")

    wf.add_step("Open Folder")

    wf.add_step("Run Python")

    print(wf.execute())

    print(wf.status())
    
