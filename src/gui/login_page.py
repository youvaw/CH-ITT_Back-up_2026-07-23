"""
=========================================
MAYAX AI - Login Page
=========================================
Project : MAYAX AI
Author  : AVISHKAR
Version : 1.2.0
=========================================
"""

import tkinter as tk

from src.auth.login import Login
from src.auth.signup_page import SignupPage


class LoginPage:

    def __init__(self, on_success=None):

        self.on_success = on_success
        self.login = Login()

        self.root = tk.Tk()
        self.root.title("MAYAX AI - Login")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#0b0f19")

        self.build_ui()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

    # =========================================
    # UI
    # =========================================

    def build_ui(self):

        container = tk.Frame(
            self.root,
            bg="#111827"
        )

        container.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=420,
            height=500
        )

        # =====================================
        # Brand
        # =====================================

        title = tk.Label(
            container,
            text="MAYAX AI",
            font=("Segoe UI", 34, "bold"),
            fg="#ffffff",
            bg="#111827"
        )

        title.pack(
            pady=(35, 0)
        )

        subtitle = tk.Label(
            container,
            text="MAYAX AI SYSTEM",
            font=("Segoe UI", 13),
            fg="#9ca3af",
            bg="#111827"
        )

        subtitle.pack(
            pady=(0, 30)
        )

        # =====================================
        # User ID
        # =====================================

        user_label = tk.Label(
            container,
            text="User ID",
            font=("Segoe UI", 11),
            fg="#d1d5db",
            bg="#111827",
            anchor="w"
        )

        user_label.pack(
            fill="x",
            padx=50
        )

        self.user_entry = tk.Entry(
            container,
            font=("Segoe UI", 12),
            bg="#1f2937",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat"
        )

        self.user_entry.pack(
            fill="x",
            padx=50,
            ipady=10,
            pady=(5, 18)
        )

        # =====================================
        # Password
        # =====================================

        password_label = tk.Label(
            container,
            text="Password",
            font=("Segoe UI", 11),
            fg="#d1d5db",
            bg="#111827",
            anchor="w"
        )

        password_label.pack(
            fill="x",
            padx=50
        )

        password_frame = tk.Frame(
            container,
            bg="#111827"
        )

        password_frame.pack(
            fill="x",
            padx=50
        )

        self.password_entry = tk.Entry(
            password_frame,
            font=("Segoe UI", 12),
            bg="#1f2937",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            show="*"
        )

        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10
        )

        self.show_button = tk.Button(
            password_frame,
            text="Show",
            command=self.toggle_password,
            bg="#1f2937",
            fg="#9ca3af",
            activebackground="#1f2937",
            activeforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            cursor="hand2"
        )

        self.show_button.pack(
            side="right",
            padx=(5, 0)
        )

        # =====================================
        # LOGIN BUTTON
        # =====================================

        login_button = tk.Button(
            container,
            text="SIGN IN",
            command=self.handle_login,
            font=("Segoe UI", 12, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            cursor="hand2"
        )

        login_button.pack(
            fill="x",
            padx=50,
            pady=(30, 12),
            ipady=10
        )

        # =====================================
        # CREATE ACCOUNT
        # =====================================

        signup_button = tk.Button(
            container,
            text="CREATE NEW ACCOUNT",
            command=self.open_signup,
            font=("Segoe UI", 10),
            bg="#111827",
            fg="#60a5fa",
            activebackground="#111827",
            activeforeground="#93c5fd",
            relief="flat",
            borderwidth=0,
            cursor="hand2"
        )

        signup_button.pack(
            pady=(0, 10)
        )

        # =====================================
        # Status
        # =====================================

        self.status_label = tk.Label(
            container,
            text="",
            font=("Segoe UI", 10),
            fg="#9ca3af",
            bg="#111827"
        )

        self.status_label.pack(
            pady=(10, 0)
        )

        # =====================================
        # ENTER KEY
        # =====================================

        self.root.bind(
            "<Return>",
            lambda event: self.handle_login()
        )

        self.user_entry.focus_set()

    # =========================================
    # Show / Hide Password
    # =========================================

    def toggle_password(self):

        if self.password_entry.cget("show") == "":

            self.password_entry.config(
                show="*"
            )

            self.show_button.config(
                text="Show"
            )

        else:

            self.password_entry.config(
                show=""
            )

            self.show_button.config(
                text="Hide"
            )

    # =========================================
    # Login
    # =========================================

    def handle_login(self):

        user_id = self.user_entry.get().strip()
        password = self.password_entry.get()

        if not user_id or not password:

            self.status_label.config(
                text="Please enter User ID and Password.",
                fg="#f59e0b"
            )

            return

        result = self.login.authenticate(
            user_id,
            password
        )

        if result:

            self.status_label.config(
                text="Login successful.",
                fg="#22c55e"
            )

            self.root.after(
                500,
                self.login_success
            )

        else:

            self.status_label.config(
                text="Invalid User ID or Password.",
                fg="#ef4444"
            )

            self.password_entry.delete(
                0,
                tk.END
            )

    # =========================================
    # Login Success
    # =========================================

    def login_success(self):

        self.login.close()
        self.root.destroy()

        if self.on_success:
            self.on_success()

    # =========================================
    # Open Signup
    # =========================================

    def open_signup(self):

        self.login.close()
        self.root.destroy()

        signup_page = SignupPage(
            on_success=self.open_login
        )

        signup_page.run()

    # =========================================
    # Open Login Again
    # =========================================

    def open_login(self):

        page = LoginPage(
            on_success=self.on_success
        )

        page.run()

    # =========================================
    # Close
    # =========================================

    def close(self):

        self.login.close()
        self.root.destroy()

    # =========================================
    # Run
    # =========================================

    def run(self):

        self.root.mainloop()


# =========================================
# Main
# =========================================

if __name__ == "__main__":

    page = LoginPage()
    page.run()
