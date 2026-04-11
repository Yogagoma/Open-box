import platform
import flet as ft
from open_box_db.models.base import SessionLocal
from open_box_db.models.employee import Employee
from open_box_db.hash import sha256_hash

def main(page: ft.Page):
    page.title = "Open box"

    # Window resolution
    page.window.width = 1280
    page.window.height = 720

    page.theme_mode = ft.ThemeMode.SYSTEM #Window theme mode by default

    #Login
    userField = ft.TextField()
    passwordField = ft.TextField()

    #Text to show errors
    errorText = ft.Text(color="red")



    def login(e):
        username = userField.value.strip()
        password = userField.value.strip()

        #Basic validations
        if not username:
            errorText.value = 'Type a user'
            page.update()
            return

        if not password:
             errorText.value = 'Type a password'
             page.update()
             return

        #Search for a user in the database
        db = SessionLocal()
        user = db.query(Employee).filter(Employee.user_name == username).first()

        if not user:
            errorText.value = "Not found"
            page.update()
            return

        if sha256_hash(password) != user.password_hash:
            errorText.value = "Incorrect password"
            page.update()
            return

        #Successfull login
        page.clean()
        page.add(ft.Text(f"Welcome, {user.name}", size=30))
        
    loginButton = ft.ElevatedButton('Login', on_click=login,align=ft.Alignment.CENTER)

    page.add(
        ft.Column(
            [
                ft.Text("Login", size=30),
                userField,
                passwordField,
                loginButton,
                errorText
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )









    



if __name__ == "__main__":
    os = platform.system()
    version = platform.release()

    # It converts the OS version into an integer if it is possible
    try:
        version_num = int(version)
    except ValueError:
        version_num = 0

    # If the operating system version is not Windows 10 or 11, the aplication will be displayed on a web browser   
    if os == "Windows" and version_num < 10:
        print(f"Detectado Windows {version}. Usando modo navegador.")
        ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    else:
        print(f"Detectado sistema compatible: {os} {version}. Usando modo escritorio.")
        ft.app(target=main)
