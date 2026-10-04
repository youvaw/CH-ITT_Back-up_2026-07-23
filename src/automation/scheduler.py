"""
=========================================
CHITT - Scheduler
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import threading
import time
from datetime import datetime


class Scheduler:

    def __init__(self):

        self.jobs = []

        self.running = False

        self.thread = None

    # ---------------------------------
    # Start Scheduler
    # ---------------------------------

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(

            target=self._loop,

            daemon=True

        )

        self.thread.start()

    # ---------------------------------
    # Stop Scheduler
    # ---------------------------------

    def stop(self):

        self.running = False

    # ---------------------------------
    # Scheduler Loop
    # ---------------------------------

    def _loop(self):

        while self.running:

            now = datetime.now()

            current = now.strftime("%H:%M")

            for job in self.jobs:

                if (

                    job["enabled"]

                    and job["time"] == current

                ):

                    try:

                        job["task"]()

                        job["last_run"] = str(now)

                    except Exception as error:

                        print(error)

            time.sleep(30)

    # ---------------------------------
    # Add Job
    # ---------------------------------

    def add(

        self,

        name,

        schedule_time,

        task

    ):

        self.jobs.append({

            "name": name,

            "time": schedule_time,

            "task": task,

            "enabled": True,

            "last_run": None

        })

    # ---------------------------------
    # Remove Job
    # ---------------------------------

    def remove(self, name):

        self.jobs = [

            job

            for job in self.jobs

            if job["name"] != name

        ]

    # ---------------------------------
    # Enable Job
    # ---------------------------------

    def enable(self, name):

        for job in self.jobs:

            if job["name"] == name:

                job["enabled"] = True

                return True

        return False

    # ---------------------------------
    # Disable Job
    # ---------------------------------

    def disable(self, name):

        for job in self.jobs:

            if job["name"] == name:

                job["enabled"] = False

                return True

        return False

    # ---------------------------------
    # List Jobs
    # ---------------------------------

    def list_jobs(self):

        return self.jobs

    # ---------------------------------
    # Status
    # ---------------------------------

    def status(self):

        return {

            "running": self.running,

            "jobs": len(self.jobs)

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "Scheduler",

            "status": "OK",

            "running": self.running

        }


if __name__ == "__main__":

    def demo():

        print("Task Executed")

    scheduler = Scheduler()

    scheduler.add(

        "Demo Task",

        "09:00",

        demo

    )

    scheduler.start()

    print(

        scheduler.status()

    )
    
