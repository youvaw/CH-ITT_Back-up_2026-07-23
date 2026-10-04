"""
=========================================
CHITT - Process Manager
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import psutil
import subprocess


class ProcessManager:

    def __init__(self):

        self.processes = {}

    # ---------------------------------
    # Start Process
    # ---------------------------------

    def start(self, command):

        try:

            process = subprocess.Popen(command)

            self.processes[process.pid] = process

            return {

                "success": True,

                "pid": process.pid

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Stop Process
    # ---------------------------------

    def stop(self, pid):

        try:

            process = psutil.Process(pid)

            process.terminate()

            return {

                "success": True,

                "pid": pid

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Kill Process
    # ---------------------------------

    def kill(self, pid):

        try:

            process = psutil.Process(pid)

            process.kill()

            return {

                "success": True,

                "pid": pid

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Restart Process
    # ---------------------------------

    def restart(self, pid):

        try:

            process = psutil.Process(pid)

            cmd = process.cmdline()

            process.kill()

            new_process = subprocess.Popen(cmd)

            return {

                "success": True,

                "new_pid": new_process.pid

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # Process Information
    # ---------------------------------

    def info(self, pid):

        try:

            process = psutil.Process(pid)

            return {

                "success": True,

                "pid": pid,

                "name": process.name(),

                "status": process.status(),

                "memory": process.memory_info().rss,

                "cpu": process.cpu_percent()

            }

        except Exception as error:

            return {

                "success": False,

                "error": str(error)

            }

    # ---------------------------------
    # List Processes
    # ---------------------------------

    def list(self):

        result = []

        for process in psutil.process_iter(

            ["pid", "name", "status"]

        ):

            result.append(

                process.info

            )

        return result

    # ---------------------------------
    # Find Process
    # ---------------------------------

    def find(self, name):

        results = []

        for process in psutil.process_iter(

            ["pid", "name"]

        ):

            if name.lower() in process.info["name"].lower():

                results.append(

                    process.info

                )

        return results

    # ---------------------------------
    # Running?
    # ---------------------------------

    def running(self, pid):

        return psutil.pid_exists(pid)

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "module": "ProcessManager",

            "running_processes": len(

                psutil.pids()

            ),

            "status": "OK"

        }


if __name__ == "__main__":

    manager = ProcessManager()

    print(

        manager.health()

    )

    print(

        manager.list()[:5]

    )
    
