import customtkinter as ctk
from PIL import Image

# ========== APP SETTINGS ==========
ctk.set_appearance_mode("light")  # Force light mode
ctk.set_default_color_theme("blue")

# Light Mode Color Palette
PINK = "#e75480"
LIGHT_PINK = "#f7a1b1"
BG_COLOR = "#f5f5f5"
CARD_COLOR = "#ffffff"
TEXT_COLOR = "#333333"
SUBTEXT_COLOR = "#666666"


class KeyVoxApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KeyVox (Light Mode)")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.configure(fg_color=BG_COLOR)
        self.current_frame = None
        self.enrollment_data = {}
        self.show_welcome_page()

    # =========================================================
    # PAGE HELPERS
    # =========================================================
    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def clear_content(self):
        if hasattr(self, 'content_frame') and self.content_frame:
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            self.content_frame.pack_forget()
            self.content_frame.grid_forget()
            self.content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

    # =========================================================
    # WELCOME PAGE
    # =========================================================
    def show_welcome_page(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        try:
            logo_img = ctk.CTkImage(Image.open("logo.png"), size=(130, 130))
            ctk.CTkLabel(frame, image=logo_img, text="").pack(pady=(80, 15))
        except Exception:
            ctk.CTkLabel(frame, text="🔑", font=("Segoe UI", 60), text_color=TEXT_COLOR).pack(pady=(80, 15))

        ctk.CTkLabel(frame, text="Welcome to KeyVox",
                     font=ctk.CTkFont(size=34, weight="bold"),
                     text_color=TEXT_COLOR).pack(pady=(0, 10))

        ctk.CTkLabel(frame,
                     text="Your voice, your key — secure and smart access control",
                     font=ctk.CTkFont(size=16),
                     text_color=SUBTEXT_COLOR).pack(pady=(0, 30))

        ctk.CTkButton(frame, text="Get Started",
                      fg_color=PINK, hover_color=LIGHT_PINK,
                      text_color="white", font=ctk.CTkFont(size=18, weight="bold"),
                      corner_radius=25, width=200, height=45,
                      command=self.show_login_page).pack(pady=(10, 40))

        ctk.CTkLabel(frame, text="© 2025 KeyVox Technologies",
                     text_color=SUBTEXT_COLOR, font=ctk.CTkFont(size=12)
                     ).pack(side="bottom", pady=20)

    # =========================================================
    # LOGIN PAGE
    # =========================================================
    def show_login_page(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        ctk.CTkButton(frame, text="← Back",
                      fg_color="transparent", hover_color="#ececec",
                      text_color=SUBTEXT_COLOR, width=100, height=35,
                      command=self.show_welcome_page).place(x=20, y=20)

        ctk.CTkLabel(frame, text="Login to KeyVox",
                     font=ctk.CTkFont(size=28, weight="bold"), text_color=PINK).pack(pady=(90, 20))

        username = ctk.CTkEntry(frame, placeholder_text="Username",
                                width=300, height=40, corner_radius=15,
                                fg_color=CARD_COLOR, border_color=PINK, border_width=2,
                                text_color=TEXT_COLOR)
        username.pack(pady=10)

        password = ctk.CTkEntry(frame, placeholder_text="Password",
                                show="•", width=300, height=40, corner_radius=15,
                                fg_color=CARD_COLOR, border_color=PINK, border_width=2,
                                text_color=TEXT_COLOR)
        password.pack(pady=10)

        ctk.CTkButton(frame, text="Login", fg_color=PINK, hover_color=LIGHT_PINK,
                      text_color="white", corner_radius=25, width=200, height=40,
                      font=ctk.CTkFont(size=16, weight="bold"),
                      command=lambda: self.fake_login(username.get(), password.get())).pack(pady=25)

        ctk.CTkButton(frame, text="No account? Enroll your voice",
                      fg_color="transparent", hover_color="#ececec",
                      text_color=PINK, width=250, height=35,
                      command=self.show_enrollment_step1).pack(pady=(5, 10))

    def fake_login(self, username, password):
        if username and password:
            self.show_dashboard(username)
        else:
            ctk.CTkLabel(self.current_frame, text="Please enter both username and password.",
                         text_color="red", font=ctk.CTkFont(size=12)).pack(pady=5)

    # =========================================================
    # DASHBOARD (LIGHT MODE)
    # =========================================================
    def show_dashboard(self, username):
        self.clear_frame()
        self.current_user = username
        dashboard = ctk.CTkFrame(self, fg_color=BG_COLOR)
        dashboard.pack(fill="both", expand=True)
        self.current_frame = dashboard

        navbar = ctk.CTkFrame(dashboard, height=90, fg_color=BG_COLOR, corner_radius=0)
        navbar.pack(side="top", fill="x")

        try:
            logo = ctk.CTkImage(Image.open("logo.png"), size=(75, 75))
            ctk.CTkLabel(navbar, image=logo, text="").pack(side="left", padx=(30, 20), pady=7)
        except:
            ctk.CTkLabel(navbar, text="KeyVox", font=ctk.CTkFont(size=36, weight="bold"),
                         text_color=TEXT_COLOR).pack(side="left", padx=30, pady=15)

        nav_frame = ctk.CTkFrame(navbar, fg_color="transparent")
        nav_frame.pack(side="left", padx=20)

        nav_font = ctk.CTkFont(size=16)
        self.home_btn = ctk.CTkButton(nav_frame, text="Home", fg_color=PINK,
                                      hover_color=LIGHT_PINK, text_color="white", font=nav_font,
                                      command=self.navigate_to_home)
        self.home_btn.pack(side="left", padx=10)

        self.apps_btn = ctk.CTkButton(nav_frame, text="Applications", fg_color="transparent",
                                      hover_color=LIGHT_PINK, text_color=TEXT_COLOR, font=nav_font,
                                      command=self.navigate_to_apps)
        self.apps_btn.pack(side="left", padx=10)

        self.profile_btn = ctk.CTkButton(nav_frame, text="User Profile", fg_color="transparent",
                                         hover_color=LIGHT_PINK, text_color=TEXT_COLOR, font=nav_font,
                                         command=self.navigate_to_profile)
        self.profile_btn.pack(side="left", padx=10)

        self.content_frame = ctk.CTkFrame(dashboard, fg_color=BG_COLOR)
        self.content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)
        
        self.navigate_to_home()

    def update_nav_style(self, active_button):
        for btn in [self.home_btn, self.apps_btn, self.profile_btn]:
            if btn == active_button:
                btn.configure(fg_color=PINK, text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_COLOR)

    # =========================================================
    # NAVIGATION HANDLERS
    # =========================================================
    def navigate_to_home(self):
        self.update_nav_style(self.home_btn)
        self.show_home()

    def navigate_to_apps(self):
        self.update_nav_style(self.apps_btn)
        self.show_applications()

    def navigate_to_profile(self):
        self.update_nav_style(self.profile_btn)
        self.show_user_profile()

    # =========================================================
    # HOME PAGE
    # =========================================================
    def show_home(self):
        self.clear_content()
        card = ctk.CTkFrame(self.content_frame, fg_color=CARD_COLOR, corner_radius=25)
        card.pack(pady=80, ipadx=60, ipady=30)

        ctk.CTkLabel(card, text="Security Token Detected",
                     text_color=TEXT_COLOR, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(30, 20))

        ctk.CTkLabel(card, text="Token ID: f3d4-9a7b-23ce-8e6f",
                     text_color=SUBTEXT_COLOR, font=ctk.CTkFont(size=14)).pack(pady=5)

        ctk.CTkLabel(card, text="Last Sync: 5 seconds ago",
                     text_color=SUBTEXT_COLOR, font=ctk.CTkFont(size=14)).pack(pady=5)

        ctk.CTkButton(card, text="Manage Applications",
                      fg_color=PINK, hover_color=LIGHT_PINK, text_color="white",
                      corner_radius=25, width=250, height=45,
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(40, 20))

    # =========================================================
    # APPLICATIONS PAGE
    # =========================================================
    def show_applications(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Manage Applications",
                     text_color=PINK, font=ctk.CTkFont(size=26, weight="bold")).pack(pady=20)

        container = ctk.CTkFrame(self.content_frame, fg_color=BG_COLOR)
        container.pack(fill="both", expand=True, padx=40, pady=30)

        cards = [
            {"title": "Password", "info1": "********", "button": "Edit Password"},
            {"title": "Voice Biometrics", "info1": "Status: Enrolled", "button": "Edit Biometrics"},
            {"title": "OTP Settings", "info1": "Account: a***@gmail.com", "button": "Edit Email Address"}
        ]

        for col, card_data in enumerate(cards):
            card_frame = ctk.CTkFrame(container, fg_color=CARD_COLOR, corner_radius=15)
            card_frame.grid(row=0, column=col, padx=15, ipadx=20, ipady=20, sticky="nsew")

            ctk.CTkLabel(card_frame, text=card_data["title"],
                         text_color=TEXT_COLOR, font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(15, 10))

            ctk.CTkLabel(card_frame, text=card_data["info1"],
                         text_color=SUBTEXT_COLOR, font=ctk.CTkFont(size=14)).pack(pady=(5, 15))

            ctk.CTkButton(card_frame, text=card_data["button"],
                          fg_color=PINK, hover_color=LIGHT_PINK,
                          text_color="white", corner_radius=20,
                          width=160, height=35).pack(pady=(10, 10))

    # =========================================================
    # USER PROFILE PAGE
    # =========================================================
    def show_user_profile(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="User Profile",
                     text_color=PINK, font=ctk.CTkFont(size=26, weight="bold")).pack(pady=30)

        fields = {
            "Name": "Ashley Jewel Heart Malasa",
            "Username": "ashley_m",
            "Email Address": "ashley.m@example.com",
            "Date of Enrollment": "October 5, 2025"
        }

        for key, value in fields.items():
            row = ctk.CTkFrame(self.content_frame, fg_color=CARD_COLOR, corner_radius=10)
            row.pack(pady=8, padx=250, fill="x")
            ctk.CTkLabel(row, text=f"{key}:", text_color=TEXT_COLOR,
                         font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(row, text=value, text_color=SUBTEXT_COLOR,
                         font=ctk.CTkFont(size=14)).pack(side="right", padx=10, pady=10)


if __name__ == "__main__":
    app = KeyVoxApp()
    app.mainloop()
