# -*- coding: utf-8 -*-

"""
MYX Launch Animation Engine

Responsible only for visual launch presentation.
It does NOT contain MYX core logic.
"""

import tkinter as tk

from src.gui import launch_config
from src.gui.launch_events import get_event


class MyXLaunchAnimation:
    def __init__(self, on_complete=None):
        self.on_complete = on_complete
        self.root = tk.Tk()

        self.root.title(launch_config.WINDOW_TITLE)
        self.root.configure(bg=launch_config.BACKGROUND)

        # Fullscreen / borderless premium launch screen
        self.root.attributes("-fullscreen", True)
        self.root.overrideredirect(True)

        self.root.bind("<Escape>", self._escape)

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self._build_ui()

        self.current_second = launch_config.COUNTDOWN_SECONDS

    def _build_ui(self):
        self.container = tk.Frame(
            self.root,
            bg=launch_config.BACKGROUND
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        self.brand = tk.Label(
            self.container,
            text="MYX",
            bg=launch_config.BACKGROUND,
            fg=launch_config.TEXT_PRIMARY,
            font=("Segoe UI Light", 72)
        )

        self.brand.place(
            relx=0.5,
            rely=0.38,
            anchor="center"
        )

        self.status = tk.Label(
            self.container,
            text="",
            bg=launch_config.BACKGROUND,
            fg=launch_config.TEXT_SECONDARY,
            font=("Segoe UI", 13)
        )

        self.status.place(
            relx=0.5,
            rely=0.53,
            anchor="center"
        )

        self.countdown = tk.Label(
            self.container,
            text="",
            bg=launch_config.BACKGROUND,
            fg=launch_config.TEXT_PRIMARY,
            font=("Segoe UI Light", 42)
        )

        self.countdown.place(
            relx=0.5,
            rely=0.62,
            anchor="center"
        )

        self.footer = tk.Label(
            self.container,
            text="MYX AI SYSTEM",
            bg=launch_config.BACKGROUND,
            fg="#444444",
            font=("Segoe UI", 9)
        )

        self.footer.place(
            relx=0.5,
            rely=0.94,
            anchor="center"
        )

    def start(self):
        if launch_config.SHOW_DEBUG:
            print("[MYX Launch] Animation started")

        self._countdown()

    def _countdown(self):
        second = self.current_second

        if second <= 0:
            self._awakening()
            return

        event_text = get_event(second)

        self.countdown.configure(
            text=str(second)
        )

        self.status.configure(
            text=event_text
        )

        if launch_config.SHOW_DEBUG:
            print(
                f"[MYX Launch] "
                f"{second} - {event_text}"
            )

        self.current_second -= 1

        self.root.after(
            launch_config.EVENT_DISPLAY_TIME_MS,
            self._countdown
        )

    def _awakening(self):
        self.countdown.configure(text="")
        self.status.configure(
            text=launch_config.AWAKENING_TEXT
        )

        self.brand.configure(
            font=("Segoe UI Light", 78)
        )

        if launch_config.SHOW_DEBUG:
            print(
                "[MYX Launch] "
                + launch_config.AWAKENING_TEXT
            )

        self.root.after(
            launch_config.AWAKENING_TIME_MS,
            self._system_online
        )

    def _system_online(self):
        self.status.configure(
            text=launch_config.ONLINE_TEXT
        )

        self.brand.configure(
            font=("Segoe UI Light", 82)
        )

        if launch_config.SHOW_DEBUG:
            print(
                "[MYX Launch] "
                + launch_config.ONLINE_TEXT
            )

        self.root.after(
            launch_config.ONLINE_TIME_MS,
            self._finish
        )

    def _finish(self):
        if launch_config.SHOW_DEBUG:
            print("[MYX Launch] Animation complete")

        self.root.destroy()

        if self.on_complete:
            self.on_complete()

    def _escape(self, event=None):
        """
        Development convenience:
        ESC closes launch animation.
        """
        self.root.destroy()


def run_launch_animation(on_complete=None):
    animation = MyXLaunchAnimation(
        on_complete=on_complete
    )

    animation.start()
    animation.root.mainloop()
    