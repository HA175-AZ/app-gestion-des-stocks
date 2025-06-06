from views.interface import Interface
from views.login import LoginWindow

def start_interface():
    app = Interface()
    app.run()

if __name__ == "__main__":
    login = LoginWindow(on_success=start_interface)
    login.run()