import flet as ft
from open_box_db.base import SessionLocal
from open_box_db.models.employee import Employee
from open_box_db.hash import sha256_hash
from datetime import date

class SignUpScreen(ft.Column):
    def __init__(self, page:ft.Page, on_navigate_login):
        super().__init__()
        self.main_page = page
        self.on_navigate_login = on_navigate_login

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER

        # UI components
        self.id_field = ft.TextField(label='ID', width=200)
        self.name_field = ft.TextField(label='First name', width=300)
        self.last_name_field = ft.TextField(label='Last name', width=300)
        self.user_name_field = ft.TextField(label='User name', width=300)
        self.phone_number_field = ft.TextField(label='Phone number', width=300)
        self.password_field = ft.TextField(label='Password', password=True,can_reveal_password=False)
        self.confirm_password_field = ft.TextField(label='Confirm password', password=True,can_reveal_password=False)

        self.feed_back_text = ft.Text() # It can be red for error, green for success

        self.sign_up_button = ft.ElevatedButton('Register', on_click=self.register)
        self.login_link = ft.TextButton('Already have an acount?, Login', on_click=self.on_navigate_login)

        self.controls = [
            ft.Text('Create account', size=30),
            self.id_field,
            self.name_field,
            self.last_name_field,
            self.user_name_field,
            self.phone_number_field,
            self.password_field,
            self.confirm_password_field,
            self.sign_up_button,
            self.login_link,
            self.feed_back_text
            ]

    def show_message(self, message, is_error=True):
        self.feed_back_text.value = message
        self.feed_back_text.color = 'red' if is_error else 'green'
        self.update()

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
        if not all([ID,name,last_name,password,confirm_password]):
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
        existing_user = db.query(Employee).filter(Employee.user_name == user_name).first()

        if existing_user:
            self.show_message('This user already exist.')
            db.close()
            return

        # Create a new employee row
        new_user = Employee(
            id=ID,
            name=name,
            last_name=last_name,
            password_hash=sha256_hash(password),
            phone_number = phone_number,
            salary=0,
            paid=False,
            start_date=date.today(),
            Type='Coach' # For now they will be preserved as coach, by default
            )

        # Save to database
        try:
            db.add(new_user)
            db.commit()
            self.show_message('Account created successfully', is_error=False)

            # Clear the fields after succesfull registration
            self.id_field.value = ''
            self.name_field.value = ''
            self.lastname_field.value = ''
            self.username_field.value = ''
            self.phone_number_field = ''
            self.password_field.value = ''
            self.confirm_password_field.value = ''
            self.update()

        except Exception as e:
            db.rollback()
            self.show_message(f'Database error:{str(e)}', is_error=True)

        finally:
            db.close()