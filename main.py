import platform
from turtle import onclick
import flet as ft
from open_box_db.base import Base, engine
from ui.screens import login_view
from ui.screens.login_view import LoginScreen
from ui.screens.sign_up_screen import SignUpScreen




def main(page: ft.Page):
    page.title = "Open box"

    # Define navigation functions
    def show_login(e=None):
        page.clean()
        # Pass show_signup as the callback
        page.add(LoginScreen(page, on_navigate_signup=show_signup))
        page.update()

    def show_signup(e=None):
        page.clean()
        # Pass show_login as the callback
        page.add(SignUpScreen(page, on_navigate_login=show_login))
        page.update()

    # Start the app on the login screen
    show_login()



    



if __name__ == "__main__":

    # Initialize database tables before running the app
    Base.metadata.create_all(bind=engine)

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
