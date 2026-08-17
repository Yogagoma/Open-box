import flet as ft
from open_box_db.base import SessionLocal
from open_box_db.models.employee import Employee
from open_box_db.hash import sha256_hash

class LoginScreen(ft.Column):
    def __init__(self, page:ft.Page, on_navigate_sign_up):
        super().__init__()
        self.main_page = page
        self.on_navigate_sign_up = on_navigate_sign_up

        # Center the content inside the column
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER

        # Define the UI components
        self.user_field =ft.TextField()
        self.password_field = ft.TextField(password=True, can_reveal_password=False)
        self.error_text = ft.Text(color="red")
        self.login_button = ft.ElevatedButton('Login', on_click=self.login)

        # Add a sign up button
        self.signup_link = ft.TextButton("Don't have an account? Sign Up", on_click=self.on_navigate_sign_up)

        # Add them to the layout's controls
        self.controls = [
            ft.Text("Login", size=30),
            self.user_field,
            self.password_field,
            self.login_button,
            self.error_text
        ]

    # It defines the event logic inside the class
    def login(self, e):
        username = self.user_field.value.strip()
        password = self.password_field.value.strip()

        # Basic validations
        if not username:
            self.error_text.value = 'Type a user'
            self.update() # update() applies to this specific component
            return

        if not password:
             self.error_text.value = 'Type a password'
             self.update()
             return

        # Database connection
        db = SessionLocal()
        user = db.query(Employee).filter(Employee.user_name == username).first()
        db.close()

        if not user:
            self.error_text.value = "Not found"
            self.update()
            return

        if sha256_hash(password) != user.password_hash:
            self.error_text.value = "Incorrect password"
            self.update()
            return

        # Successful login - manipulate the main page
        self.main_page.clean()
        self.main_page.add(ft.Text(f"Welcome, {user.name}", size=30))
        self.main_page.update()


