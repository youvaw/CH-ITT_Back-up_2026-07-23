from src.system.app_manager import AppManager # type: ignore

app = AppManager()

print("Opening Notepad...")
app.open_app("notepad")

input("Press Enter to close Notepad...")

app.close_app("notepad.exe")

print("Done")

