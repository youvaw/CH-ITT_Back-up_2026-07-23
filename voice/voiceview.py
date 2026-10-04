# ============================================================
# VOICE VIEW
# ============================================================

class VoiceView(ctk.CTkFrame):

    def __init__(self, parent, brain=None):
        super().__init__(parent)

        self.brain = brain
        self.voice_engine = None
        self.is_running = False

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

        self.voice_engine = MyXVoiceEngine(
            brain=self.brain,
            on_status=self.on_voice_status,
            on_text=self.on_voice_text,
            on_response=self.on_voice_response
        )

        threading.Thread(
            target=self._run_voice_engine,
            daemon=True
        ).start()

    def _run_voice_engine(self):

        try:
            self.voice_engine.start()

        except Exception as e:

            self.after(
                0,
                lambda error=e:
                self._show_error(error)
            )

        finally:

            self.after(
                0,
                self._voice_engine_finished
            )

    def _voice_engine_finished(self):

        self.is_running = False

        self.start_btn.configure(
            state="normal"
        )

        self.stop_btn.configure(
            state="normal"
        )

        self._draw_idle_wave()

        self._set_status(
            "Idle",
            "blue"
        )

    def stop_voice(self):

        if self.voice_engine is not None:

            try:
                self.voice_engine.stop()
            except Exception as e:
                print(f"[VoiceView] Stop warning: {e}")

        self.is_running = False

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
        