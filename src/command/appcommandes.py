import os


class AppCommands:

    def open_notepad(self):

        os.system("start notepad")
        return True

    def open_calculator(self):

        os.system("start calc")
        return True

    def open_cmd(self):

        os.system("start cmd")
        return True
    
