"""
=========================================
CHITT - Task Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""


class TaskManager:

    def __init__(self):

        self.tasks = []

    # ---------------------------------
    # Add Task
    # ---------------------------------

    def add(self, task_name):

        task = {

            "id": len(self.tasks) + 1,

            "task": task_name,

            "status": "Pending"

        }

        self.tasks.append(task)

        return task

    # ---------------------------------
    # Complete Task
    # ---------------------------------

    def complete(self, task_id):

        for task in self.tasks:

            if task["id"] == task_id:

                task["status"] = "Completed"

                return True

        return False

    # ---------------------------------
    # Delete Task
    # ---------------------------------

    def delete(self, task_id):

        for task in self.tasks:

            if task["id"] == task_id:

                self.tasks.remove(task)

                return True

        return False

    # ---------------------------------
    # Get Task
    # ---------------------------------

    def get(self, task_id):

        for task in self.tasks:

            if task["id"] == task_id:

                return task

        return None

    # ---------------------------------
    # Get All Tasks
    # ---------------------------------

    def list(self):

        return self.tasks

    # ---------------------------------
    # Pending Tasks
    # ---------------------------------

    def pending(self):

        return [

            task

            for task in self.tasks

            if task["status"] == "Pending"

        ]

    # ---------------------------------
    # Completed Tasks
    # ---------------------------------

    def completed(self):

        return [

            task

            for task in self.tasks

            if task["status"] == "Completed"

        ]

    # ---------------------------------
    # Clear Tasks
    # ---------------------------------

    def clear(self):

        self.tasks.clear()

    # ---------------------------------
    # Total Tasks
    # ---------------------------------

    def count(self):

        return len(self.tasks)

    # ---------------------------------
    # Show Tasks
    # ---------------------------------

    def show(self):

        print("\n===== TASK LIST =====\n")

        if not self.tasks:

            print("No Tasks Available.")

            return

        for task in self.tasks:

            print(

                f"[{task['id']}] "

                f"{task['task']} "

                f"({task['status']})"

            )


if __name__ == "__main__":

    manager = TaskManager()

    manager.add("Open YouTube")

    manager.add("Backup Project")

    manager.complete(1)

    manager.show()
    
