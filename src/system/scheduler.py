"""
CHITT Background Task Scheduler
"""

import threading
import time

from logger.logger import Logger


class Scheduler:

    def __init__(self):

        self.logger = Logger()

        self.tasks = {}

        self.running = False

    # ==================================================
    # Add Task
    # ==================================================

    def add_task(self, name, function, interval):

        self.tasks[name] = {

            "function": function,

            "interval": interval,

            "last_run": 0

        }

        self.logger.info(f"Task Added : {name}")

    # ==================================================
    # Remove Task
    # ==================================================

    def remove_task(self, name):

        if name in self.tasks:

            del self.tasks[name]

            self.logger.info(f"Task Removed : {name}")

    # ==================================================
    # Execute Tasks
    # ==================================================

    def _loop(self):

        while self.running:

            current = time.time()

            for task in self.tasks.values():

                if current - task["last_run"] >= task["interval"]:

                    try:

                        task["function"]()

                        task["last_run"] = current

                    except Exception as error:

                        self.logger.error(error)

            time.sleep(1)

    # ==================================================
    # Start Scheduler
    # ==================================================

    def start(self):

        if self.running:

            return

        self.running = True

        thread = threading.Thread(

            target=self._loop,

            daemon=True

        )

        thread.start()

        self.logger.info("Scheduler Started")

    # ==================================================
    # Stop Scheduler
    # ==================================================

    def stop(self):

        self.running = False

        self.logger.info("Scheduler Stopped")

    # ==================================================
    # Built-in Tasks
    # ==================================================

    @staticmethod
    def auto_save():

        print("[Scheduler] Auto Saving...")

    @staticmethod
    def memory_cleanup():

        print("[Scheduler] Memory Cleanup...")

    @staticmethod
    def auto_backup():

        print("[Scheduler] Database Backup...")

    @staticmethod
    def plugin_refresh():

        print("[Scheduler] Plugin Refresh...")

    @staticmethod
    def health_check():

        print("[Scheduler] System Health Check...")


if __name__ == "__main__":

    scheduler = Scheduler()

    scheduler.add_task(

        "AutoSave",

        scheduler.auto_save,

        5

    )

    scheduler.add_task(

        "Memory",

        scheduler.memory_cleanup,

        10

    )

    scheduler.add_task(

        "Backup",

        scheduler.auto_backup,

        15

    )

    scheduler.add_task(

        "Plugins",

        scheduler.plugin_refresh,

        20

    )

    scheduler.add_task(

        "Health",

        scheduler.health_check,

        25

    )

    scheduler.start()

    try:

        while True:

            time.sleep(1)

    except KeyboardInterrupt:

        scheduler.stop()
        
