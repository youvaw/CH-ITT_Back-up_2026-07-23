# -*- coding: utf-8 -*-
"""MyX sign-in, account setup, and Windows account binding UI."""

import os
import re
import bcrypt
import customtkinter as ctk
from tkinter import messagebox

from src.security.email_recovery import email_recovery_status
from src.security.myx_auth_store import AuthStore, AuthStoreError, MyXAuthService, find_user_key


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))


class MyXAuthApp(ctk.CTk):
    def __init__(self, on_login_success=None):
        super().__init__()
        self.on_login_success = on_login_success
        self.mode = "login"
        self.password_visible = False
        self._binding_authorized_username = None
        self.auth_service = None
        self.title("MyX AI Assistant")
        self.geometry("620x820")
        self.minsize(560, 700)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.build_ui()
        try:
            self.auth_service = MyXAuthService(AuthStore(project_root=BASE_DIR))
        except AuthStoreError:
            self.show_message("MyX authentication data could not be loaded. Existing account files were preserved.", "red")
        except Exception:
            self.show_message("MyX authentication could not be initialized. Existing account files were preserved.", "red")
        self.after(0, self._attempt_windows_sign_in)

    def build_ui(self):
        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=22)
        self.main_frame.pack(padx=28, pady=24, fill="both", expand=True)

        self.logo_label = ctk.CTkLabel(self.main_frame, text="MyX", font=ctk.CTkFont(size=44, weight="bold"))
        self.logo_label.pack(pady=(28, 5))
        self.subtitle_label = ctk.CTkLabel(self.main_frame, text="Welcome to MyX AI Assistant", font=ctk.CTkFont(size=16))
        self.subtitle_label.pack(pady=(0, 24))

        self.username_entry = ctk.CTkEntry(self.main_frame, width=380, height=46, placeholder_text="Username")
        self.password_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.password_entry = ctk.CTkEntry(self.password_frame, width=320, height=46, placeholder_text="Password", show="*")
        self.password_entry.pack(side="left")
        self.password_toggle = ctk.CTkButton(self.password_frame, text="👁", width=55, height=46, command=self.toggle_password)
        self.password_toggle.pack(side="left", padx=(5, 0))
        self.password_confirm_entry = ctk.CTkEntry(self.main_frame, width=380, height=46, placeholder_text="Confirm Password", show="*")
        self.secret_entry = ctk.CTkEntry(self.main_frame, width=380, height=46, placeholder_text="Recovery Key", show="*")
        self.secret_confirm_entry = ctk.CTkEntry(self.main_frame, width=380, height=46, placeholder_text="Confirm Recovery Key", show="*")
        self.email_entry = ctk.CTkEntry(self.main_frame, width=380, height=46, placeholder_text="Recovery Email (optional)")
        self.bind_windows_var = ctk.BooleanVar(value=False)
        self.bind_windows_checkbox = ctk.CTkCheckBox(self.main_frame, text="Bind this account to the current Windows account", variable=self.bind_windows_var)

        self.main_button = ctk.CTkButton(self.main_frame, width=380, height=50, text="Sign In", font=ctk.CTkFont(size=16, weight="bold"), command=self.handle_action)
        self.account_button = ctk.CTkButton(self.main_frame, width=380, height=42, text="Create Account", fg_color="transparent", border_width=1, command=self.switch_account_mode)
        self.windows_button = ctk.CTkButton(self.main_frame, width=380, height=42, text="Sign in with Windows Account", fg_color="transparent", border_width=1, command=self.sign_in_with_windows)
        self.forgot_button = ctk.CTkButton(self.main_frame, width=380, height=40, text="Forgot Password?", fg_color="transparent", border_width=0, command=self.switch_to_reset)
        self.message_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=13), wraplength=480)
        self.update_ui()

    def _form_widgets(self):
        return (
            self.username_entry, self.password_frame, self.password_confirm_entry,
            self.secret_entry, self.secret_confirm_entry, self.email_entry,
            self.bind_windows_checkbox, self.main_button, self.account_button,
            self.windows_button, self.forgot_button, self.message_label,
        )

    def update_ui(self):
        for widget in self._form_widgets():
            widget.pack_forget()

        if self.mode == "login":
            self.subtitle_label.configure(text="Welcome to MyX AI Assistant")
            self.password_entry.configure(placeholder_text="Password")
            self.secret_entry.configure(placeholder_text="Recovery Key")
            self.main_button.configure(text="Sign In")
            self.account_button.configure(text="Create Account")
            self.forgot_button.configure(text="Forgot Password?", command=self.switch_to_reset)
            self.username_entry.pack(pady=8)
            self.password_frame.pack(pady=8)
            self.secret_entry.pack(pady=8)
            self.main_button.pack(pady=(18, 8))
            self.account_button.pack(pady=5)
            self.windows_button.pack(pady=5)
            self.forgot_button.pack(pady=2)
            self.message_label.pack(pady=(12, 4))
        elif self.mode == "signup":
            self.subtitle_label.configure(text="Create your MyX Account")
            self.password_entry.configure(placeholder_text="Create Password")
            self.secret_entry.configure(placeholder_text="Create Recovery Key")
            self.main_button.configure(text="Create Account")
            self.account_button.configure(text="Already have an account? Sign In")
            self.forgot_button.configure(text="Back to Sign In", command=self.switch_account_mode)
            self.username_entry.pack(pady=6)
            self.password_frame.pack(pady=6)
            self.password_confirm_entry.pack(pady=6)
            self.secret_entry.pack(pady=6)
            self.secret_confirm_entry.pack(pady=6)
            self.email_entry.pack(pady=6)
            self.bind_windows_checkbox.pack(pady=8)
            self.main_button.pack(pady=(14, 7))
            self.account_button.pack(pady=5)
            self.forgot_button.pack(pady=2)
            self.message_label.pack(pady=(10, 4))
        else:
            self.mode = "reset"
            self.subtitle_label.configure(text="Recover your MyX Account")
            self.password_entry.configure(placeholder_text="New Password")
            self.secret_entry.configure(placeholder_text="Recovery Key")
            self.main_button.configure(text="Reset Password")
            self.account_button.configure(text="Back to Sign In")
            self.username_entry.pack(pady=8)
            self.password_frame.pack(pady=8)
            self.secret_entry.pack(pady=8)
            self.main_button.pack(pady=(18, 8))
            self.account_button.pack(pady=5)
            self.message_label.pack(pady=(10, 4))
            self.show_message(email_recovery_status(), "orange")

    def toggle_password(self):
        self.password_visible = not self.password_visible
        self.password_entry.configure(show="" if self.password_visible else "*")
        self.password_toggle.configure(text="🙈" if self.password_visible else "👁")

    def switch_account_mode(self):
        self.mode = "signup" if self.mode == "login" else "login"
        self.clear_fields()
        self.update_ui()

    def switch_to_reset(self):
        self.mode = "reset"
        self.clear_fields()
        self.update_ui()

    def clear_fields(self):
        for entry in (self.username_entry, self.password_entry, self.password_confirm_entry, self.secret_entry, self.secret_confirm_entry, self.email_entry):
            entry.delete(0, "end")
        self.bind_windows_var.set(False)
        self.message_label.configure(text="")

    def show_message(self, message, color=None):
        options = {"text": str(message)}
        if color:
            options["text_color"] = color
        self.message_label.configure(**options)

    def _require_auth_service(self):
        if self.auth_service is None:
            self.show_message("Authentication storage is unavailable. Account changes and sign-in are disabled.", "red")
            return False
        return True

    def find_user_key(self, users, username):
        return find_user_key(users, username)

    def setup_windows_binding(self, username):
        if self._binding_authorized_username is None or self._binding_authorized_username.casefold() != username.strip().casefold():
            raise AuthStoreError("Explicit MyX sign-in and Windows binding confirmation are required.")
        self.auth_service.setup_windows_binding(username, user_authorized=True)

    def is_windows_user_bound(self):
        return bool(self.auth_service and self.auth_service.is_windows_user_bound())

    def authenticate_current_windows_user(self):
        if not self.auth_service:
            return None
        return self.auth_service.authenticate_current_windows_user()

    def _attempt_windows_sign_in(self):
        if not self.auth_service:
            return
        try:
            username = self.authenticate_current_windows_user()
            if username:
                self.open_main_project(username)
        except Exception:
            # Auto sign-in must fail closed and leave manual login available.
            self.show_message("Windows account sign-in is unavailable. Use MyX sign-in.", "orange")

    def sign_in_with_windows(self):
        if not self._require_auth_service():
            return
        try:
            username = self.authenticate_current_windows_user()
        except Exception:
            username = None
        if username:
            self.open_main_project(username)
        else:
            self.show_message("This Windows account is not bound to a MyX account.", "orange")

    def handle_action(self):
        if self.mode == "login":
            self.handle_login()
        elif self.mode == "signup":
            self.handle_signup()
        else:
            self.handle_reset()

    def handle_signup(self):
        if not self._require_auth_service():
            return
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        password_confirm = self.password_confirm_entry.get()
        recovery_key = self.secret_entry.get()
        recovery_confirm = self.secret_confirm_entry.get()
        recovery_email = self.email_entry.get().strip()

        if not username:
            self.show_message("Please enter a username.")
            return
        if not password or len(password) < 6:
            self.show_message("Password must contain at least 6 characters.")
            return
        if password != password_confirm:
            self.show_message("Passwords do not match.")
            return
        if not recovery_key:
            self.show_message("Please create a recovery key.")
            return
        if recovery_key != recovery_confirm:
            self.show_message("Recovery keys do not match.")
            return
        if recovery_email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", recovery_email):
            self.show_message("Enter a valid recovery email or leave the field blank.")
            return

        bind_now = bool(self.bind_windows_var.get())
        try:
            self.auth_service.create_account(username, password, recovery_key, recovery_email, bind_to_current_windows_user=bind_now)
        except AuthStoreError as exc:
            self.show_message(str(exc), "red")
            return
        except Exception:
            self.show_message("Account setup failed. No account was activated.", "red")
            return

        if recovery_email:
            status = "Account created. Email recovery is not configured; use the recovery key."
            color = "orange"
        elif bind_now:
            status = "Account created and bound to this Windows account."
            color = "green"
        else:
            status = "Account created. Windows sign-in is not enabled for this account."
            color = "orange"
        self.mode = "login"
        self.clear_fields()
        self.update_ui()
        self.show_message(status, color)

    def handle_login(self):
        if not self._require_auth_service():
            return
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username:
            self.show_message("Please enter your username.")
            return
        if not password:
            self.show_message("Please enter your password.")
            return
        try:
            authenticated_username = self.auth_service.authenticate_password(username, password)
        except AuthStoreError:
            self.show_message("MyX authentication data is invalid or unavailable. Existing account files were preserved.", "red")
            return
        except Exception:
            self.show_message("Unable to verify this MyX account.", "red")
            return
        if authenticated_username is None:
            self.show_message("Username or password is incorrect.")
            return

        if not self.auth_service.is_windows_user_bound(authenticated_username):
            should_bind = messagebox.askyesno(
                "Bind Windows Account",
                "MyX sign-in succeeded. Bind this MyX account to the current Windows account for future sign-in?",
                parent=self,
            )
            if should_bind:
                self._binding_authorized_username = authenticated_username
                try:
                    self.setup_windows_binding(authenticated_username)
                    self.show_message("Windows account binding saved.", "green")
                except Exception:
                    self.show_message("MyX sign-in succeeded, but Windows account binding could not be saved.", "orange")
                finally:
                    self._binding_authorized_username = None

        self.show_message("Login successful. Opening MyX Dashboard...", "green")
        self.after(500, lambda name=authenticated_username: self.open_main_project(name))

    def handle_reset(self):
        if not self._require_auth_service():
            return
        username = self.username_entry.get().strip()
        new_password = self.password_entry.get()
        recovery_key = self.secret_entry.get()
        if not username:
            self.show_message("Please enter your username.")
            return
        if not new_password or len(new_password) < 6:
            self.show_message("New password must contain at least 6 characters.")
            return
        if not recovery_key:
            self.show_message("Please enter your recovery key.")
            return
        try:
            data = self.auth_service.store.load()
            stored_username = self.find_user_key(data["users"], username)
            if stored_username is None:
                self.show_message("Username not found.")
                return
            account = data["users"][stored_username]
            if not self.auth_service.verify_recovery_key(recovery_key, account.get("secret_hash", "")):
                self.show_message("Recovery key is incorrect.")
                return
            account["password_hash"] = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")
            self.auth_service.store.save(data)
        except AuthStoreError:
            self.show_message("MyX authentication data is invalid or unavailable.", "red")
            return
        except Exception:
            self.show_message("Unable to complete password recovery.", "red")
            return
        messagebox.showinfo("MyX Password", "Password reset successfully.", parent=self)
        self.mode = "login"
        self.clear_fields()
        self.update_ui()

    def open_main_project(self, username):
        try:
            self.destroy()
            if self.on_login_success:
                self.on_login_success(username)
        except Exception:
            # Do not include authentication material in error output.
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    app = MyXAuthApp()
    app.mainloop()
