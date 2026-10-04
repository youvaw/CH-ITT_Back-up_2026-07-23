# -*- coding: utf-8 -*-

import threading

import cv2
import numpy as np
import customtkinter as ctk
from PIL import Image

from src.voice.voice_engine import MyXVoiceEngine


# ============================================================
# MEMORY VIEW
# ============================================================

class MemoryView(ctk.CTkFrame):

    def __init__(self, parent, brain=None):

        super().__init__(parent)

        self.brain = brain

        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="System Memory Logs",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(
            side="left",
            padx=10
        )

        self.refresh_btn = ctk.CTkButton(
            self.header_frame,
            text="Refresh Memory",
            command=self.load_memory
        )
        self.refresh_btn.pack(
            side="right",
            padx=10
        )

        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            width=600,
            height=400
        )
        self.scroll_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.load_memory()

    def load_memory(self):

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if self.brain is None:

            ctk.CTkLabel(
                self.scroll_frame,
                text="MyX Brain is not connected."
            ).pack(pady=20)

            return

        try:

            history = self.brain.get_conversation_history()

            if not history:

                ctk.CTkLabel(
                    self.scroll_frame,
                    text="No conversation history saved yet."
                ).pack(pady=20)

                return

            # Show newest conversations first.
            history = list(reversed(history[-50:]))

            for row in history:

                role = ""
                message = ""
                timestamp = ""

                if isinstance(row, dict):

                    role = row.get("role", "")
                    message = row.get("message", "")
                    timestamp = row.get(
                        "timestamp",
                        row.get("created_at", "")
                    )

                else:

                    try:

                        role = row["role"]
                        message = row["message"]
                        timestamp = row["timestamp"]

                    except Exception:

                        try:
                            role = row[2]
                            message = row[3]
                            timestamp = row[4]
                        except Exception:
                            continue

                card = ctk.CTkFrame(
                    self.scroll_frame
                )

                card.pack(
                    fill="x",
                    pady=5,
                    padx=5
                )

                role_text = str(role).upper()

                ctk.CTkLabel(
                    card,
                    text=f"{role_text}",
                    font=("Arial", 11, "bold")
                ).pack(
                    anchor="w",
                    padx=10,
                    pady=(6, 0)
                )

                ctk.CTkLabel(
                    card,
                    text=str(message),
                    font=("Arial", 12),
                    wraplength=700,
                    justify="left"
                ).pack(
                    anchor="w",
                    padx=10,
                    pady=3
                )

                if timestamp:

                    ctk.CTkLabel(
                        card,
                        text=str(timestamp),
                        font=("Arial", 9, "italic"),
                        text_color="gray"
                    ).pack(
                        anchor="w",
                        padx=10,
                        pady=(0, 6)
                    )

        except Exception as e:

            ctk.CTkLabel(
                self.scroll_frame,
                text=f"Error loading memory: {e}",
                text_color="red"
            ).pack(pady=20)


# ============================================================
# VISION VIEW
# ============================================================

class VisionView(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.cap = None
        self.is_camera_running = False

        self.title_label = ctk.CTkLabel(
            self,
            text="MAYAX Vision Mode",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=10)

        self.video_label = ctk.CTkLabel(
            self,
            text="Camera Preview",
            width=640,
            height=360,
            fg_color="black"
        )
        self.video_label.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            self,
            text="Camera: OFF",
            text_color="red",
            font=("Arial", 12, "bold")
        )
        self.status_label.pack(pady=5)

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)

        self.start_btn = ctk.CTkButton(
            self.btn_frame,
            text="Start Camera",
            command=self.start_camera
        )
        self.start_btn.pack(
            side="left",
            padx=5
        )

        self.stop_btn = ctk.CTkButton(
            self.btn_frame,
            text="Stop Camera",
            command=self.stop_camera
        )
        self.stop_btn.pack(
            side="left",
            padx=5
        )

    def start_camera(self):

        if self.is_camera_running:
            return

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():

            self.status_label.configure(
                text="Camera Error: Device not found!",
                text_color="red"
            )

            self.cap.release()
            self.cap = None

            return

        self.is_camera_running = True

        self.status_label.configure(
            text="Camera: ON",
            text_color="green"
        )

        self.update_frame()

    def update_frame(self):

        if not self.is_camera_running:
            return

        if self.cap is None:
            return

        ret, frame = self.cap.read()

        if ret:

            cv2_image = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            img = Image.fromarray(cv2_image)

            img_tk = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(640, 360)
            )

            self.video_label.configure(
                image=img_tk,
                text=""
            )

            self.video_label.image = img_tk

        self.after(
            15,
            self.update_frame
        )

    def stop_camera(self):

        self.is_camera_running = False

        if self.cap is not None:

            self.cap.release()
            self.cap = None

        self.video_label.configure(
            image="",
            text="Camera Preview"
        )

        self.status_label.configure(
            text="Camera: OFF",
            text_color="red"
        )


# ============================================================
# VOICE VIEW
# ============================================================

class VoiceView(ctk.CTkFrame):

    def __init__(self, parent, brain=None):
        super().__init__(parent)

        self.brain = brain
        self.voice_engine = None
        self.is_running = False
        self._voice_run_id = 0

        self.title_label = ctk.CTkLabel(
            self,
            text="MAYAX Voice Engine",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Idle",
            text_color="blue",
            font=("Arial", 14)
        )
        self.status_label.pack(pady=5)

        self.result_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 12),
            wraplength=700,
            justify="center"
        )
        self.result_label.pack(padx=20, pady=5)

        self.canvas = ctk.CTkCanvas(
            self,
            width=400,
            height=150,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack(pady=15)

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)

        self.start_btn = ctk.CTkButton(
            self.btn_frame,
            text="Start Voice",
            command=self.start_voice
        )
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ctk.CTkButton(
            self.btn_frame,
            text="Stop Voice",
            command=self.stop_voice
        )
        self.stop_btn.pack(side="left", padx=5)

        self._draw_idle_wave()

    def _draw_idle_wave(self):
        self.canvas.delete("all")

        self.canvas.create_line(
            10,
            75,
            390,
            75,
            fill="#00FF66",
            width=2
        )

    def _draw_active_wave(self):
        if not self.is_running:
            self._draw_idle_wave()
            return

        self.canvas.delete("all")

        bars = 30
        bar_width = 8
        center_y = 75

        for i in range(bars):
            amplitude = np.random.randint(5, 50)
            x = i * 13 + 10

            self.canvas.create_rectangle(
                x,
                center_y - amplitude,
                x + bar_width,
                center_y + amplitude,
                fill="#00FF66",
                outline=""
            )

        self.after(80, self._draw_active_wave)

    def _set_status(self, text, color="blue"):
        self.after(
            0,
            lambda: self.status_label.configure(
                text=f"Status: {text}",
                text_color=color
            )
        )

    def on_voice_status(self, message):
        self._set_status(str(message), "green")

    def on_voice_text(self, text):
        self.after(
            0,
            lambda: self.result_label.configure(
                text=f"You: {text}"
            )
        )

    def on_voice_response(self, response):
        self.after(
            0,
            lambda: self.result_label.configure(
                text=f"MyX: {response}"
            )
        )

    def start_voice(self):

        if self.is_running:
            return

        if self.brain is None:
            self._set_status(
                "Core Brain not connected.",
                "red"
            )
            return

        self._voice_run_id += 1
        run_id = self._voice_run_id
        self.is_running = True

        self.start_btn.configure(
            state="disabled"
        )

        self.stop_btn.configure(
            state="normal"
        )

        self._set_status(
            "Starting Voice Engine...",
            "green"
        )

        self._draw_active_wave()

        try:
            threading.Thread(
                target=self._run_voice_engine,
                args=(run_id,),
                daemon=True
            ).start()

        except Exception as e:
            self.is_running = False
            self._voice_run_id += 1
            self.start_btn.configure(state="normal")
            self._show_error(e)

    def _run_voice_engine(self, run_id):

        error = None

        try:
            if run_id != self._voice_run_id or not self.is_running:
                return

            # Construction loads OpenWakeWord, so it belongs on this worker.
            engine = MyXVoiceEngine(
                brain=self.brain,
                on_status=self.on_voice_status,
                on_text=self.on_voice_text,
                on_response=self.on_voice_response
            )

            self.voice_engine = engine

            # Stop may have been requested while the model was loading.
            if run_id != self._voice_run_id or not self.is_running:
                engine.stop()
                return

            engine.start()

        except Exception as e:
            error = e

        finally:
            if run_id == self._voice_run_id:
                self.after(
                    0,
                    lambda current_run=run_id, current_error=error:
                    self._voice_engine_finished(
                        current_run,
                        current_error
                    )
                )

    def _voice_engine_finished(self, run_id, error=None):

        # Ignore completion from a stopped or superseded worker.
        if run_id != self._voice_run_id:
            return

        self.is_running = False
        self.voice_engine = None

        self.start_btn.configure(
            state="normal"
        )

        self.stop_btn.configure(
            state="normal"
        )

        self._draw_idle_wave()

        if error is not None:
            self._show_error(error)
            return

        self._set_status(
            "Idle",
            "blue"
        )

    def stop_voice(self):

        # Invalidate any worker still constructing the engine.
        self._voice_run_id += 1
        self.is_running = False

        engine = self.voice_engine
        self.voice_engine = None

        if engine is not None:
            try:
                engine.stop()
            except Exception as e:
                print(f"[VoiceView] Stop warning: {e}")

        self.start_btn.configure(
            state="normal"
        )

        self._draw_idle_wave()

        self._set_status(
            "Stopped",
            "orange"
        )

    def _show_error(self, error):

        self.result_label.configure(
            text=f"Voice Error: {error}"
        )

        self.status_label.configure(
            text="Status: Error",
            text_color="red"
        )

class ChatView(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        brain=None,
        username="User"
    ):

        super().__init__(parent)

        self.brain = brain
        self.username = username

        self.chat_display = ctk.CTkScrollableFrame(
            self,
            width=600,
            height=400
        )
        self.chat_display.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.input_frame = ctk.CTkFrame(
            self
        )
        self.input_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Ask MAYAX something..."
        )
        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            pady=5
        )

        self.entry.bind(
            "<Return>",
            lambda event: self.send_message()
        )

        self.send_btn = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=80,
            command=self.send_message
        )
        self.send_btn.pack(
            side="right",
            padx=5,
            pady=5
        )

    def send_message(self):

        user_text = self.entry.get().strip()

        if not user_text:
            return

        self.add_message(
            f"User: {user_text}",
            align="e",
            bg_color="#1f538d"
        )

        self.entry.delete(
            0,
            "end"
        )

        if self.brain:

            try:

                response = self.brain.process(
                    user_text
                )

            except Exception as e:

                response = f"System Error: {e}"

        else:

            response = (
                "MAYAX Core Brain is not connected."
            )

        self.add_message(
            f"MAYAX: {response}",
            align="w",
            bg_color="#2b2b2b"
        )

    def add_message(
        self,
        text,
        align="w",
        bg_color="#2b2b2b"
    ):

        msg_card = ctk.CTkFrame(
            self.chat_display,
            fg_color=bg_color
        )

        msg_card.pack(
            anchor=align,
            pady=5,
            padx=5
        )

        lbl = ctk.CTkLabel(
            msg_card,
            text=text,
            font=("Arial", 12),
            wraplength=450,
            justify="left"
        )

        lbl.pack(
            padx=10,
            pady=5
        )


# ============================================================
# MAIN WINDOW
# ============================================================

class MainWindow(ctk.CTk):

    def __init__(self, brain=None):

        super().__init__()

        self.brain = brain

        self.title(
            "MAYAX AI - Control Center"
        )

        self.geometry(
            "1100x700"
        )

        ctk.set_appearance_mode(
            "Dark"
        )

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        self.header_frame = ctk.CTkFrame(
            self,
            height=50,
            corner_radius=0
        )

        self.header_frame.pack(
            side="top",
            fill="x"
        )

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="MAYAX AI SYSTEM",
            font=("Arial", 20, "bold")
        )

        self.title_label.pack(
            pady=10
        )

        # ----------------------------------------------------
        # Body
        # ----------------------------------------------------

        self.body_frame = ctk.CTkFrame(
            self
        )

        self.body_frame.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Sidebar
        # ----------------------------------------------------

        self.sidebar = ctk.CTkFrame(
            self.body_frame,
            width=180,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y",
            padx=5,
            pady=5
        )

        # ----------------------------------------------------
        # Content
        # ----------------------------------------------------

        self.container = ctk.CTkFrame(
            self.body_frame
        )

        self.container.pack(
            side="right",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # ----------------------------------------------------
        # Screens
        # ----------------------------------------------------

        self.frames = {

            "Chat":
                ChatView(
                    self.container,
                    brain=self.brain
                ),

            "Voice":
                VoiceView(
                    self.container,
                    brain=self.brain
                ),

            "Vision":
                VisionView(
                    self.container
                ),

            "Memory":
                MemoryView(
                    self.container,
                    brain=self.brain
                ),
        }

        for frame in self.frames.values():

            frame.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

        self.container.grid_rowconfigure(
            0,
            weight=1
        )

        self.container.grid_columnconfigure(
            0,
            weight=1
        )

        # ----------------------------------------------------
        # Navigation
        # ----------------------------------------------------

        nav_buttons = [
            ("Chat", "Chat"),
            ("Voice", "Voice"),
            ("Vision", "Vision"),
            ("Memory", "Memory"),
        ]

        for text, name in nav_buttons:

            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=lambda n=name:
                self.show_frame(n)
            )

            btn.pack(
                fill="x",
                padx=10,
                pady=8
            )

        self.show_frame(
            "Chat"
        )

    def show_frame(self, name):

        frame = self.frames.get(name)

        if frame:
            frame.tkraise()

            if name == "Memory":
                frame.load_memory()

    def run(self):

        self.mainloop()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 55)
    print("       MAYAX MAIN WINDOW TEST")
    print("=" * 55)

    app = MainWindow(
        brain=None
    )

    app.mainloop()
    

