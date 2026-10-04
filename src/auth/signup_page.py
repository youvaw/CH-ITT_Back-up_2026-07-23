"""
=========================================
MAYAX AI - Create Account
=========================================
Project : MAYAX AI
Author  : AVISHKAR
Version : 2.1.0
=========================================
"""

import tkinter as tk

from src.auth.signup import Signup


class SignupPage:

    def __init__(self):

        self.signup = Signup()

        self.root = tk.Tk()
        self.root.title("MAYAX AI - Create Account")
        self.root.geometry("500x850")
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
            height=790
        )

        # =====================================
        # BRAND
        # =====================================

        title = tk.Label(
            container,
            text="MAYAX AI",
            font=("Segoe UI", 34, "bold"),
            fg="#ffffff",
            bg="#111827"
        )

        title.pack(pady=(25, 0))

        subtitle = tk.Label(
            container,
            text="CREATE NEW ACCOUNT",
            font=("Segoe UI", 13),
            fg="#9ca3af",
            bg="#111827"
        )

        subtitle.pack(pady=(0, 20))

        # =====================================
        # USER ID
        # =====================================

        self.user_id = self.create_field(
            container,
            "User ID"
        )

        # =====================================
        # NAME
        # =====================================

        self.name = self.create_field(
            container,
            "Name"
        )

        # =====================================
        # NICKNAME
        # =====================================

        self.nickname = self.create_field(
            container,
            "Nickname"
        )

        # =====================================
        # EMAIL
        # =====================================

        self.email = self.create_field(
            container,
            "Email"
        )

        # =====================================
        # PHONE
        # =====================================

        self.phone = self.create_field(
            container,
            "Phone"
        )

        # =====================================
        # PASSWORD
        # =====================================

        self.password = self.create_field(
            container,
            "Password",
            show="•"
        )

        # =====================================
        # CONFIRM PASSWORD
        # =====================================

        self.confirm_password = self.create_field(
            container,
            "Confirm Password",
            show="•"
        )

        # =====================================
        # CREATE ACCOUNT
        # =====================================

        create_button = tk.Button(
            container,
            text="CREATE ACCOUNT",
            command=self.handle_signup,
            font=("Segoe UI", 12, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            cursor="hand2"
        )

        create_button.pack(
            fill="x",
            padx=45,
            pady=(15, 10),
            ipady=10
        )

        # =====================================
        # SIGN IN
        # =====================================

        signin_button = tk.Button(
            container,
            text="SIGN IN",
            command=self.open_login,
            font=("Segoe UI", 11, "bold"),
            bg="#111827",
            fg="#60a5fa",
            activebackground="#111827",
            activeforeground="#93c5fd",
            relief="flat",
            borderwidth=0,
            cursor="hand2"
        )

        signin_button.pack(
            pady=(5, 5)
        )

        # =====================================
        # STATUS
        # =====================================

        self.status_label = tk.Label(
            container,
            text="",
            font=("Segoe UI", 10),
            fg="#9ca3af",
            bg="#111827"
        )

        self.status_label.pack(
            pady=(5, 0)
        )

        self.user_id.focus_set()

    # =========================================
    # FIELD CREATOR
    # =========================================

    def create_field(
        self,
        parent,
        label_text,
        show=None
    ):

        label = tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 10),
            fg="#d1d5db",
            bg="#111827",
            anchor="w"
        )

        label.pack(
            fill="x",
            padx=45
        )

        entry = tk.Entry(
            parent,
            font=("Segoe UI", 12),
            bg="#1f2937",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat"
        )

        if show:
            entry.config(show=show)

        entry.pack(
            fill="x",
            padx=45,
            ipady=8,
            pady=(3, 10)
        )

        return entry

    # =========================================
    # SIGNUP
    # =========================================

    def handle_signup(self):

        user_id = self.user_id.get().strip()
        name = self.name.get().strip()
        nickname = self.nickname.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        password = self.password.get()
        confirm_password = self.confirm_password.get()

        # -------------------------------------
        # Basic Validation
        # -------------------------------------

        if not user_id or not name or not password:
            self.show_status(
                "Please fill User ID, Name and Password.",
                "#f59e0b"
            )
            return

        if password != confirm_password:
            self.show_status(
                "Passwords do not match.",
                "#ef4444"
            )
            return

        # -------------------------------------
        # Register
        # -------------------------------------

        try:

            result = self.signup.register(
                user_id=user_id,
                name=name,
                password=password,
                nickname=nickname,
                email=email,
                phone=phone
            )

            if result:

                self.show_status(
                    "Account created successfully.",
                    "#22c55e"
                )

                self.root.after(
                    1000,
                    self.open_login
                )

            else:

                self.show_status(
                    "User ID already exists.",
                    "#ef4444"
                )

        except ValueError as error:

            self.show_status(
                str(error),
                "#ef4444"
            )

        except Exception as error:

            self.show_status(
                f"Signup error: {error}",
                "#ef4444"
            )

    # =========================================
    # STATUS
    # =========================================

    def show_status(
        self,
        message,
        color
    ):

        self.status_label.config(
            text=message,
            fg=color
        )

    # =========================================
    # OPEN LOGIN
    # =========================================

    def open_login(self):

        self.signup.close()
        self.root.destroy()

        # Import here to avoid circular import
        from src.gui.login_page import LoginPage

        login_page = LoginPage()
        login_page.run()

    # =========================================
    # CLOSE
    # =========================================

    def close(self):

        self.signup.close()
        self.root.destroy()

    # =========================================
    # RUN
    # =========================================

    def run(self):

        self.root.mainloop()


# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    page = SignupPage()
    page.run()
