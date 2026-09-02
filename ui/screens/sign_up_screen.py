import flet as ft
from open_box_db.base import SessionLocal
from open_box_db.models.employee import Employee
from open_box_db.hash import sha256_hash
from datetime import date

# ── Design tokens ─────────────────────────────────────────────────
_CARD_BG       = "#1a1a2e"
_PRIMARY       = "#6c63ff"
_PRIMARY_HVR   = "#5a52d5"
_TEXT_PRIMARY   = "#e0e0e0"
_TEXT_SECONDARY = "#8888a0"
_FIELD_BG      = "#16162b"
_FIELD_BORDER  = "#2a2a45"
_ERROR_COLOR   = "#ff5252"
_SUCCESS_COLOR = "#69f0ae"


def _styled_field(
    label: str,
    icon: str,
    *,
    password: bool = False,
    width: int | None = None,
    expand: bool = False,
) -> ft.TextField:
    """Return a consistently‑styled dark TextField."""
    return ft.TextField(
        label=label,
        prefix_icon=icon,
        password=password,
        can_reveal_password=password,
        width=width,
        expand=expand,
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
        width=420,
        height=48,
        bgcolor=_PRIMARY,
        color=ft.Colors.WHITE,
        elevation=4,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )


class SignUpScreen(ft.Column):
    def __init__(self, page: ft.Page, on_navigate_login):
        super().__init__()
        self.main_page = page
        self.on_navigate_login = on_navigate_login

        # Full‑height centred column
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.CENTER

        # ── Form fields ───────────────────────────────────────────
        self.id_field = _styled_field("Employee ID", ft.Icons.BADGE_OUTLINED, width=180)
        self.name_field = _styled_field("First name", ft.Icons.PERSON_OUTLINE_ROUNDED, expand=True)
        self.last_name_field = _styled_field("Last name", ft.Icons.PERSON_OUTLINE_ROUNDED, expand=True)
        self.user_name_field = _styled_field("Username", ft.Icons.ACCOUNT_CIRCLE_OUTLINED, width=420)
        self.phone_number_field = _styled_field("Phone number", ft.Icons.PHONE_OUTLINED, width=420)
        self.password_field = _styled_field("Password", ft.Icons.LOCK_OUTLINE_ROUNDED, password=True, expand=True)
        self.confirm_password_field = _styled_field("Confirm password", ft.Icons.LOCK_OUTLINE_ROUNDED, password=True, expand=True)

        # Feedback banner (hidden until needed)
        self.feed_back_icon = ft.Icon(ft.Icons.FEEDBACK, size=16)
        self.feed_back_text = ft.Text(size=13, text_align=ft.TextAlign.CENTER)
        self.feed_back_container = ft.Container(
            content=ft.Row(
                [self.feed_back_icon, self.feed_back_text],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6,
            ),
            border_radius=8,
            padding=ft.Padding(14, 8, 14, 8),
            visible=False,
            width=420,
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )

        # ── Card content ──────────────────────────────────────────
        card_content = ft.Container(
            width=500,
            padding=ft.Padding(40, 32, 40, 32),
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
                spacing=16,
                scroll=ft.ScrollMode.AUTO,
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
                        content=ft.Icon(ft.Icons.PERSON_ADD_ROUNDED, color=ft.Colors.WHITE, size=32),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=20,
                            color=ft.Colors.with_opacity(0.4, _PRIMARY),
                            offset=ft.Offset(0, 4),
                        ),
                    ),
                    # ── Title ─────────────────────────────────────
                    ft.Text(
                        "Create account",
                        size=26,
                        weight=ft.FontWeight.W_700,
                        color=_TEXT_PRIMARY,
                    ),
                    ft.Text(
                        "Fill in your details to register",
                        size=14,
                        color=_TEXT_SECONDARY,
                    ),
                    ft.Container(height=2),  # spacer

                    # ── ID field (narrower, standalone) ───────────
                    self.id_field,

                    # ── Name row ──────────────────────────────────
                    ft.Row(
                        [self.name_field, self.last_name_field],
                        spacing=12,
                        width=420,
                    ),

                    # ── Username & phone ──────────────────────────
                    self.user_name_field,
                    self.phone_number_field,

                    # ── Password row ──────────────────────────────
                    ft.Row(
                        [self.password_field, self.confirm_password_field],
                        spacing=12,
                        width=420,
                    ),

                    # ── Feedback banner ───────────────────────────
                    self.feed_back_container,

                    # ── Register button ───────────────────────────
                    _primary_button("Register", self.register),

                    # ── Login link ────────────────────────────────
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Already have an account?", size=13, color=_TEXT_SECONDARY),
                            ft.TextButton(
                                content=ft.Text("Login", color=_PRIMARY),
                                on_click=self.on_navigate_login,
                            ),
                        ],
                    ),
                ],
            ),
        )

        self.controls = [card_content]

    # ── Helpers ───────────────────────────────────────────────────
    def show_message(self, message, is_error=True):
        self.feed_back_text.value = message
        if is_error:
            self.feed_back_text.color = _ERROR_COLOR
            self.feed_back_icon.name = ft.Icons.ERROR_OUTLINE_ROUNDED
            self.feed_back_icon.color = _ERROR_COLOR
            self.feed_back_container.bgcolor = "#2b1a1a"
        else:
            self.feed_back_text.color = _SUCCESS_COLOR
            self.feed_back_icon.name = ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED
            self.feed_back_icon.color = _SUCCESS_COLOR
            self.feed_back_container.bgcolor = "#1a2b1a"
        self.feed_back_container.visible = True
        self.update()

    # ── Registration logic ────────────────────────────────────────
    def register(self, e):
        ID = self.id_field.value.strip()
        name = self.name_field.value.strip()
        last_name = self.last_name_field.value.strip()
        user_name = self.user_name_field.value.strip()
        phone_number = self.phone_number_field.value.strip()
        password = self.password_field.value.strip()
        confirm_password = self.confirm_password_field.value.strip()

        # Validations
        # All fields are required
        if not all([ID, name, last_name, user_name, password, confirm_password]):
            self.show_message('All fields are required.')
            return

        # The passwords must match
        if password != confirm_password:
            self.show_message('Passwords do not match.')
            return

        # Convert the phone number to an integer
        try:
            phone_number = int(phone_number)
        except ValueError:
            # If they typed letters, symbols, or spaces inside the number, catch it here
            self.show_message('Phone number must contain only numbers.')
            return

        # Convert the ID to an integer
        try:
            ID = int(ID)
        except ValueError:
            self.show_message('ID must contain only numbers.')
            return

        # Open a db session
        db = SessionLocal()

        # Check if username exist
        existing_user = db.query(Employee).filter(Employee.user_name == user_name).first()

        if existing_user:
            self.show_message('This user already exists.')
            db.close()
            return

        # Create a new employee row
        new_user = Employee(
            id=ID,
            name=name,
            last_name=last_name,
            user_name=user_name,
            password_hash=sha256_hash(password),
            phone_number=phone_number,
            salary_per_month=0,
            paid=False,
            start_date=date.today(),
            Type='Coach'  # For now they will be preserved as coach, by default
        )

        # Save to database
        try:
            db.add(new_user)
            db.commit()
            self.show_message('Account created successfully!', is_error=False)

            # Clear the fields after successful registration
            self.id_field.value = ''
            self.name_field.value = ''
            self.last_name_field.value = ''
            self.user_name_field.value = ''
            self.phone_number_field.value = ''
            self.password_field.value = ''
            self.confirm_password_field.value = ''
            self.update()

        except Exception as ex:
            db.rollback()
            self.show_message(f'Database error: {str(ex)}', is_error=True)

        finally:
            db.close()