import os


class SystemCommands:

    def shutdown(self):

        os.system("shutdown /s /t 5")
        return True

    def restart(self):

        os.system("shutdown /r /t 5")
        return True

    def lock(self):

        os.system("rundll32.exe user32.dll,LockWorkStation")
        return True
    
