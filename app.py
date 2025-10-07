import customtkinter as ctk
from PIL import Image

# ========== APP SETTINGS ==========
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

PINK = "#e75480"
LIGHT_PINK = "#f28ca0"
BG_COLOR = "#1a1a1a"
CARD_COLOR = "#2b2b2b"
TEXT_COLOR = "white"
SUBTEXT_COLOR = "gray80"


class KeyVoxApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KeyVox")
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
            ctk.CTkLabel(frame, text="🔑", font=("Segoe UI", 60)).pack(pady=(80, 15))

        ctk.CTkLabel(frame, text="Welcome to KeyVox",
                     font=ctk.CTkFont(size=34, weight="bold"),
                     text_color="white").pack(pady=(0, 10))

        ctk.CTkLabel(frame,
                     text="Your voice, your key — secure and smart access control",
                     font=ctk.CTkFont(size=16),
                     text_color="gray80").pack(pady=(0, 30))

        ctk.CTkButton(frame, text="Get Started",
                      fg_color=PINK, hover_color=LIGHT_PINK,
                      text_color="white", font=ctk.CTkFont(size=18, weight="bold"),
                      corner_radius=25, width=200, height=45,
                      command=self.show_login_page).pack(pady=(10, 40))

        ctk.CTkLabel(frame, text="© 2025 KeyVox Technologies",
                     text_color="gray60", font=ctk.CTkFont(size=12)
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
                      fg_color="transparent", hover_color="#2e2e2e",
                      text_color="gray80", width=100, height=35,
                      command=self.show_welcome_page).place(x=20, y=20)

        ctk.CTkLabel(frame, text="Login to KeyVox",
                     font=ctk.CTkFont(size=28, weight="bold"), text_color=PINK).pack(pady=(90, 20))

        username = ctk.CTkEntry(frame, placeholder_text="Username",
                                width=300, height=40, corner_radius=15,
                                fg_color=CARD_COLOR, border_color=PINK, border_width=2,
                                text_color="white")
        username.pack(pady=10)

        password = ctk.CTkEntry(frame, placeholder_text="Password",
                                show="•", width=300, height=40, corner_radius=15,
                                fg_color=CARD_COLOR, border_color=PINK, border_width=2,
                                text_color="white")
        password.pack(pady=10)

        ctk.CTkButton(frame, text="Login", fg_color=PINK, hover_color=LIGHT_PINK,
                      text_color="white", corner_radius=25, width=200, height=40,
                      font=ctk.CTkFont(size=16, weight="bold"),
                      command=lambda: self.fake_login(username.get(), password.get())).pack(pady=25)

        ctk.CTkButton(frame, text="No account? Enroll your voice",
                      fg_color="transparent", hover_color="#2e2e2e",
                      text_color=LIGHT_PINK, width=250, height=35,
                      command=self.show_enrollment_step1).pack(pady=(5, 10))

    def fake_login(self, username, password):
        if username and password:
            self.show_dashboard(username)
        else:
            ctk.CTkLabel(self.current_frame, text="Please enter both username and password.",
                         text_color="red", font=ctk.CTkFont(size=12)).pack(pady=5)

    # =========================================================
    # ENROLLMENT PAGES (STEP 1–3 + SUMMARY)
    # =========================================================
    def show_enrollment_step1(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        ctk.CTkLabel(frame, text="Enrollment - Step 1: User Information",
                     text_color=PINK, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)

        entries = {}
        for field in ["Full Name", "Username", "Password", "Confirm Password", "Email Address"]:
            entry = ctk.CTkEntry(frame, placeholder_text=field, width=300, height=40,
                                 corner_radius=15, fg_color=CARD_COLOR, border_color=PINK, border_width=2,
                                 text_color="white", show="•" if "Password" in field else "")
            entry.pack(pady=8)
            entries[field] = entry

        ctk.CTkButton(frame, text="Next", fg_color=PINK, hover_color=LIGHT_PINK,
                      width=200, height=40, corner_radius=25,
                      command=lambda: self.store_enrollment_data(entries)).pack(pady=25)

        ctk.CTkButton(frame, text="← Back", fg_color="transparent",
                      text_color="gray80", hover_color="#2e2e2e",
                      command=self.show_login_page).pack(pady=5)

    def store_enrollment_data(self, entries):
        self.enrollment_data = {field: entry.get() for field, entry in entries.items()}
        self.show_enrollment_step2()

    def show_enrollment_step2(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        ctk.CTkLabel(frame, text="Enrollment - Step 2: Voice Enrollment",
                     text_color=PINK, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)

        for i in range(1, 6):
            ctk.CTkLabel(frame, text=f"Voice Phrase {i}: \"This is my secure voice.\"",
                         text_color="white", font=ctk.CTkFont(size=16)).pack(pady=5)
            ctk.CTkButton(frame, text=f"Record Phrase {i}", fg_color=PINK, hover_color=LIGHT_PINK,
                          width=200, height=35, corner_radius=25).pack(pady=5)

        ctk.CTkButton(frame, text="Next", fg_color=PINK, hover_color=LIGHT_PINK,
                      width=200, height=40, corner_radius=25,
                      command=self.show_enrollment_step3).pack(pady=25)

        ctk.CTkButton(frame, text="← Back", fg_color="transparent",
                      text_color="gray80", hover_color="#2e2e2e",
                      command=self.show_enrollment_step1).pack(pady=5)

    def show_enrollment_step3(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        ctk.CTkLabel(frame, text="Enrollment - Step 3: OTP Verification",
                     text_color=PINK, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)

        ctk.CTkLabel(frame, text="Enter the 6-digit code sent to your email address:",
                     text_color="white", font=ctk.CTkFont(size=16)).pack(pady=10)
        otp = ctk.CTkEntry(frame, width=150, height=40, corner_radius=15,
                           fg_color=CARD_COLOR, border_color=PINK, border_width=2,
                           text_color="white")
        otp.pack(pady=10)

        ctk.CTkButton(frame, text="Send Code", fg_color=PINK, hover_color=LIGHT_PINK,
                      width=150, height=35, corner_radius=25).pack(pady=5)
        ctk.CTkButton(frame, text="Verify", fg_color=PINK, hover_color=LIGHT_PINK,
                      width=150, height=35, corner_radius=25,
                      command=self.show_enrollment_summary).pack(pady=20)

        ctk.CTkButton(frame, text="← Back", fg_color="transparent",
                      text_color="gray80", hover_color="#2e2e2e",
                      command=self.show_enrollment_step2).pack(pady=5)

    def show_enrollment_summary(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        ctk.CTkLabel(frame, text="Enrollment Complete!",
                     text_color=PINK, font=ctk.CTkFont(size=26, weight="bold")).pack(pady=30)

        for k, v in self.enrollment_data.items():
            ctk.CTkLabel(frame, text=f"{k}: {v}", text_color="white",
                         font=ctk.CTkFont(size=14)).pack(pady=2)

        ctk.CTkButton(frame, text="Proceed to Dashboard", fg_color=PINK,
                      hover_color=LIGHT_PINK, corner_radius=25,
                      width=250, height=40,
                      command=lambda: self.show_dashboard(self.enrollment_data.get("Username", "User"))).pack(pady=30)

    # =========================================================
    # DASHBOARD + NAVIGATION (NAVBAR VERSION)
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
            logo_label = ctk.CTkLabel(navbar, image=logo, text="")
            logo_label.pack(side="left", padx=(30, 20), pady=7)
        except:
            logo_label = ctk.CTkLabel(navbar, text="KeyVox", font=ctk.CTkFont(size=36, weight="bold"))
            logo_label.pack(side="left", padx=30, pady=15)
        
        nav_frame = ctk.CTkFrame(navbar, fg_color="transparent")
        nav_frame.pack(side="left", padx=20)

        nav_font = ctk.CTkFont(size=16)
        self.home_btn = ctk.CTkButton(nav_frame, text="Home", fg_color=PINK,
                                      hover_color=LIGHT_PINK, text_color="white", font=nav_font,
                                      command=self.navigate_to_home)
        self.home_btn.pack(side="left", padx=10)

        self.apps_btn = ctk.CTkButton(nav_frame, text="Applications", fg_color="transparent",
                                      hover_color=LIGHT_PINK, text_color="white", font=nav_font,
                                      command=self.navigate_to_apps)
        self.apps_btn.pack(side="left", padx=10)

        self.profile_btn = ctk.CTkButton(nav_frame, text="User Profile", fg_color="transparent",
                                        hover_color=LIGHT_PINK, text_color="white", font=nav_font,
                                        command=self.navigate_to_profile)
        self.profile_btn.pack(side="left", padx=10)

        status_frame = ctk.CTkFrame(navbar, fg_color="transparent")
        status_frame.pack(side="right", padx=30)
        
        ctk.CTkLabel(status_frame, text="status", text_color="gray80").pack(side="left", padx=10)
        try:
            help_icon = ctk.CTkImage(Image.open("help.png"), size=(24, 24))
            help_button = ctk.CTkButton(status_frame, image=help_icon, text="", fg_color="transparent",
                                        width=24, height=24, hover_color="#2e2e2e",
                                        command=self.show_help_page)
            help_button.pack(side="left", padx=5)

            about_icon = ctk.CTkImage(Image.open("about.png"), size=(24, 24))
            about_button = ctk.CTkButton(status_frame, image=about_icon, text="", fg_color="transparent",
                                         width=24, height=24, hover_color="#2e2e2e",
                                         command=self.show_about_page)
            about_button.pack(side="left", padx=5)
        except Exception as e:
            print(f"Icon error: {e}. Using text buttons as fallback.")
            help_fallback = ctk.CTkButton(status_frame, text="?", font=ctk.CTkFont(size=16, weight="bold"),
                                          fg_color="transparent", width=24, height=24,
                                          hover_color="#2e2e2e", command=self.show_help_page)
            help_fallback.pack(side="left", padx=5)
            
            about_fallback = ctk.CTkButton(status_frame, text="i", font=ctk.CTkFont(size=16, weight="bold"),
                                           fg_color="transparent", width=24, height=24,
                                           hover_color="#2e2e2e", command=self.show_about_page)
            about_fallback.pack(side="left", padx=5)


        self.content_frame = ctk.CTkFrame(dashboard, fg_color=BG_COLOR)
        self.content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)
        
        self.navigate_to_home()

    def update_nav_style(self, active_button):
        for btn in [self.home_btn, self.apps_btn, self.profile_btn]:
            if btn == active_button:
                btn.configure(fg_color=PINK)
            else:
                btn.configure(fg_color="transparent")

    # --- Navigation wrapper methods ---
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

        try:
            key_icon = ctk.CTkImage(Image.open("key.png"), size=(50, 50))
            mic_icon = ctk.CTkImage(Image.open("mic.png"), size=(50, 50))
            otp_icon = ctk.CTkImage(Image.open("otp.png"), size=(50, 50))
        except Exception:
            key_icon = mic_icon = otp_icon = None

        cards = [
            {"icon": key_icon, "title": "Password", "info1": "********", "button": "Edit Password"},
            {"icon": mic_icon, "title": "Voice Biometrics", "info1": "Status: Enrolled", "button": "Edit Biometrics"},
            {"icon": otp_icon, "title": "OTP Settings", "info1": "Account: a***@gmail.com", "button": "Edit Email Address"}
        ]

        for i in range(3):
            container.grid_columnconfigure(i, weight=1, uniform="equal")

        for col, card_data in enumerate(cards):
            card_frame = ctk.CTkFrame(container, fg_color=CARD_COLOR, corner_radius=15)
            card_frame.grid(row=0, column=col, padx=15, ipadx=20, ipady=20, sticky="nsew")

            if card_data["icon"]:
                ctk.CTkLabel(card_frame, image=card_data["icon"], text="").pack(pady=(15, 10))

            ctk.CTkLabel(card_frame, text=card_data["title"],
                         text_color="white", font=ctk.CTkFont(size=18, weight="bold")).pack()

            ctk.CTkLabel(card_frame, text=card_data["info1"],
                         text_color="white", font=ctk.CTkFont(size=14)).pack(pady=(5, 15))

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
            ctk.CTkLabel(row, text=f"{key}:", text_color="white",
                         font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(row, text=value, text_color="gray80",
                         font=ctk.CTkFont(size=14)).pack(side="right", padx=10, pady=10)

        ctk.CTkButton(self.content_frame, text="Deactivate Account",
                      fg_color=PINK, hover_color=LIGHT_PINK,
                      width=220, height=40, corner_radius=25,
                      command=self.show_welcome_page).pack(pady=40)

    # =========================================================
    # ABOUT PAGE
    # =========================================================
    def show_about_page(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="About KeyVox",
                     text_color=PINK, font=ctk.CTkFont(size=26, weight="bold")).pack(pady=30)

        about_text = """
KeyVox is a cutting-edge voice biometrics security application designed to provide
secure and convenient access control. Leveraging advanced AI, KeyVox identifies
users by their unique voice patterns, offering a robust alternative to traditional
passwords and tokens.

Our mission is to enhance digital security through innovative and user-friendly
solutions. With KeyVox, your voice truly becomes your key.

Version: 1.0.0
Developed by: KeyVox Technologies
© 2025 All Rights Reserved.
        """
        ctk.CTkLabel(self.content_frame, text=about_text,
                     text_color="white", font=ctk.CTkFont(size=16), justify="left").pack(pady=20, padx=50)

        try:
            logo_img = ctk.CTkImage(Image.open("logo.png"), size=(80, 80))
            ctk.CTkLabel(self.content_frame, image=logo_img, text="").pack(pady=20)
        except:
            pass

    # =========================================================
    # HELP PAGE
    # =========================================================
    def show_help_page(self):
        self.clear_content()

        # --- Create a scrollable frame inside the content frame ---
        scrollable_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color=BG_COLOR,
            corner_radius=10
        )
        scrollable_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # --- Page Title ---
        ctk.CTkLabel(
            scrollable_frame,
            text="Help & Support",
            text_color=PINK,
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(pady=30)

        # --- Help Sections ---
        help_sections = {
            "Getting Started": "Learn how to enroll your voice and set up your applications.",
            "Troubleshooting Voice Enrollment": "Tips for successful voice enrollment and common issues.",
            "Managing Applications": "How to add, remove, and configure your applications with KeyVox.",
            "Account Security": "Best practices for keeping your account secure.",
            "Contact Support": "Reach out to our support team for personalized assistance."
        }

        for title, description in help_sections.items():
            section_frame = ctk.CTkFrame(
                scrollable_frame,
                fg_color=CARD_COLOR,
                corner_radius=10
            )
            section_frame.pack(pady=10, padx=100, fill="x")

            # Section title
            ctk.CTkLabel(
                section_frame,
                text=title,
                text_color="white",
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(anchor="w", padx=20, pady=(10, 5))

            # Section description
            ctk.CTkLabel(
                section_frame,
                text=description,
                text_color="gray80",
                font=ctk.CTkFont(size=14),
                wraplength=500,
                justify="left"
            ).pack(anchor="w", padx=20, pady=(0, 10))

            # "View Details" button
            ctk.CTkButton(
                section_frame,
                text="View Details",
                fg_color="transparent",
                text_color=LIGHT_PINK,
                hover_color="#2e2e2e",
                width=120,
                height=30
            ).pack(anchor="e", padx=20, pady=(0, 10))

        # --- Footer ---
        ctk.CTkLabel(
            scrollable_frame,
            text="For urgent issues, please email support@keyvox.com",
            text_color="gray60",
            font=ctk.CTkFont(size=12)
        ).pack(pady=30)


if __name__ == "__main__":
    app = KeyVoxApp()
    app.mainloop()