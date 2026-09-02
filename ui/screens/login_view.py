import flet as ft
from open_box_db.base import SessionLocal
from open_box_db.models.employee import Employee
from open_box_db.hash import sha256_hash

# ── Design tokens ─────────────────────────────────────────────────
_CARD_BG       = "#1a1a2e"
_PRIMARY       = "#6c63ff"
_PRIMARY_HVR   = "#5a52d5"
_TEXT_PRIMARY   = "#e0e0e0"
_TEXT_SECONDARY = "#8888a0"
_FIELD_BG      = "#16162b"
_FIELD_BORDER  = "#2a2a45"
_ERROR_COLOR   = "#ff5252"


def _styled_field(
    label: str,
    icon: str,
    *,
    password: bool = False,
    width: int | None = None,
) -> ft.TextField:
    """Return a consistently‑styled dark TextField."""
    return ft.TextField(
        label=label,
        prefix_icon=icon,
        password=password,
        can_reveal_password=password,
        width=width,
        border=ft.InputBorder.OUTLINE,
        border_radius=12,
        border_color=_FIELD_BORDER,
        focused_border_color=_PRIMARY,
        bgcolor=_FIELD_BG,
        label_style=ft.TextStyle(color=_TEXT_SECONDARY, size=13),
        text_style=ft.TextStyle(color=_TEXT_PRIMARY, size=14),
        cursor_color=_PRIMARY,
        content_padding=ft.Padding(16, 14, 16, 14),
    )


def _primary_button(label: str, on_click) -> ft.Button:
    """Full‑width accent button with hover effect."""
    return ft.Button(
        content=ft.Text(label, size=15, weight=ft.FontWeight.W_600),
        on_click=on_click,
        width=360,
        height=48,
        bgcolor=_PRIMARY,
        color=ft.Colors.WHITE,
        elevation=4,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )


class LoginScreen(ft.Column):
    def __init__(self, page: ft.Page, on_navigate_sign_up):
        super().__init__()
        self.main_page = page
        self.on_navigate_sign_up = on_navigate_sign_up

        # Full‑height centred column
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER

        # ── Fields ────────────────────────────────────────────────
        self.user_field = _styled_field("Username", ft.Icons.PERSON_OUTLINE_ROUNDED, width=360)
        self.password_field = _styled_field("Password", ft.Icons.LOCK_OUTLINE_ROUNDED, password=True, width=360)

        # Error banner (hidden until needed)
        self.error_text = ft.Text(size=13, color=_ERROR_COLOR, text_align=ft.TextAlign.CENTER)
        self.error_container = ft.Container(
            content=ft.Row(
                [ft.Icon(ft.Icons.ERROR_OUTLINE_ROUNDED, color=_ERROR_COLOR, size=16), self.error_text],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6,
            ),
            bgcolor="#2b1a1a",
            border_radius=8,
            padding=ft.Padding(14, 8, 14, 8),
            visible=False,
            width=360,
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )

        # ── Card content ──────────────────────────────────────────
        card_content = ft.Container(
            width=420,
            padding=ft.Padding(30, 36, 30, 36),
            border_radius=20,
            bgcolor=_CARD_BG,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=40,
                color=ft.Colors.with_opacity(0.35, "#000000"),
                offset=ft.Offset(0, 8),
            ),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    # ── Icon badge ────────────────────────────────
                    ft.Container(
                        width=72,
                        height=72,
                        border_radius=36,
                        gradient=ft.LinearGradient(
                            colors=[_PRIMARY, "#8b83ff"],
                            begin=ft.Alignment(-1, -1),
                            end=ft.Alignment(1, 1),
                        ),
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(ft.Icons.LOCK_OPEN_ROUNDED, color=ft.Colors.WHITE, size=32),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=20,
                            color=ft.Colors.with_opacity(0.4, _PRIMARY),
                            offset=ft.Offset(0, 4),
                        ),
                    ),
                    # ── Title ─────────────────────────────────────
                    ft.Text(
                        "Welcome back",
                        size=26,
                        weight=ft.FontWeight.W_700,
                        color=_TEXT_PRIMARY,
                    ),
                    ft.Text(
                        "Sign in to continue",
                        size=14,
                        color=_TEXT_SECONDARY,
                    ),
                    ft.Container(height=4),  # spacer

                    # ── Fields ────────────────────────────────────
                    self.user_field,
                    self.password_field,

                    # ── Error banner ──────────────────────────────
                    self.error_container,

                    # ── Login button ──────────────────────────────
                    _primary_button("Login", self.login),

                    # ── Sign‑up link ──────────────────────────────
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Don't have an account?", size=13, color=_TEXT_SECONDARY),
                            ft.TextButton(
                                content=ft.Text("Sign Up", color=_PRIMARY),
                                on_click=self.on_navigate_sign_up,
                            ),
                        ],
                    ),
                ],
            ),
        )

        self.controls = [card_content]

    # ── Helpers ───────────────────────────────────────────────────
    def _show_error(self, message: str):
        self.error_text.value = message
        self.error_container.visible = True
        self.update()

    def _hide_error(self):
        self.error_container.visible = False
        self.update()

    # ── Login logic (unchanged) ───────────────────────────────────
    def login(self, e):
        username = self.user_field.value.strip()
        password = self.password_field.value.strip()

        # Basic validations
        if not username:
            self._show_error("Please enter your username")
            return

        if not password:
            self._show_error("Please enter your password")
            return

        self._hide_error()

        # Database connection
        db = SessionLocal()
        user = db.query(Employee).filter(Employee.user_name == username).first()
        db.close()

        if not user:
            self._show_error("User not found")
            return

        if sha256_hash(password) != user.password_hash:
            self._show_error("Incorrect password")
            return

        # Successful login - manipulate the main page
        self.main_page.clean()
        self.main_page.add(ft.Text(f"Welcome, {user.name}", size=30))
        self.main_page.update()
