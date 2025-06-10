from views.interface import Interface
from views.login import LoginWindow

def start_interface():
    app = Interface(on_logout=start_login)
    app.run()

def start_login():
    login = LoginWindow(on_success=start_interface)
    login.run()

if __name__ == "__main__":
    start_login()