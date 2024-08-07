import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import requests
import gui_setup

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Summer Project")
        self.setGeometry(100, 100, 400, 250)  # Initial window size
        self.center()

        self.create_login_form()

    def create_login_form(self):
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout(central_widget)

        # Title label
        self.label_title = QtWidgets.QLabel("Welcome!", self)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(self.label_title)

        # Form layout
        self.form_layout = QtWidgets.QFormLayout()

        # Username
        self.label_username = QtWidgets.QLabel("Username:", self)
        self.label_username.setStyleSheet("font-size: 14px;")
        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Enter your username")
        self.username.setStyleSheet("padding: 5px; font-size: 14px;")
        self.form_layout.addRow(self.label_username, self.username)

        # Password
        self.label_password = QtWidgets.QLabel("Password:", self)
        self.label_password.setStyleSheet("font-size: 14px;")
        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setStyleSheet("padding: 5px; font-size: 14px;")

        # Password layout
        password_layout = QtWidgets.QHBoxLayout()
        password_layout.addWidget(self.password)

        # Show Password button
        self.show_password_button = QtWidgets.QPushButton(self)
        self.show_password_button.setCheckable(True)
        self.show_password_button.setFixedSize(30, 30)
        self.show_password_button.setIcon(QtGui.QIcon(gui_setup.image1_path))
        self.show_password_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                border-radius: 5px;
            }
            QPushButton:checked {
                background-color: #45a049;
            }
        """
        )
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.show_password_button)

        self.form_layout.addRow(self.label_password, password_layout)

        main_layout.addLayout(self.form_layout)

        # Button layout
        button_layout = QtWidgets.QHBoxLayout()
        self.login_button = QtWidgets.QPushButton("Login", self)
        self.login_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        )
        self.login_button.clicked.connect(self.check_login)
        button_layout.addStretch()
        button_layout.addWidget(self.login_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        # Create Account button
        self.create_account_button = QtWidgets.QPushButton("Create an Account", self)
        self.create_account_button.setStyleSheet(
            """
            QPushButton {
                background-color: #008CBA;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005F6B;
            }
        """
        )
        self.create_account_button.clicked.connect(self.switch_to_create_account)
        main_layout.addWidget(self.create_account_button)

        # Message label
        self.message_label = QtWidgets.QLabel("", self)
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: red;")
        main_layout.addWidget(self.message_label)

    def switch_to_create_account(self):
        # Clear existing layout
        layout = self.centralWidget().layout()
        if layout:
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

        # Reset form for account creation
        self.create_account_form()

        # Add create_account_button back to the layout
        main_layout = self.centralWidget().layout()
        main_layout.addWidget(self.create_account_button)

    def create_account_form(self):
        main_layout = self.centralWidget().layout()

        # Adjust title for account creation
        self.label_title.setText("Create an Account")

        # Clear login button if exists
        if self.login_button:
            main_layout.removeWidget(self.login_button)
            self.login_button.deleteLater()

        # Create and add create_account_button
        self.create_account_button = QtWidgets.QPushButton("Create Account", self)
        self.create_account_button.setStyleSheet(
            """
            QPushButton {
                background-color: #008CBA;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005F6B;
            }
        """
        )
        self.create_account_button.clicked.connect(self.create_account)
        main_layout.addWidget(self.create_account_button)

    def toggle_password_visibility(self):
        if self.show_password_button.isChecked():
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.show_password_button.setIcon(QtGui.QIcon(gui_setup.image2_path))
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)
            self.show_password_button.setIcon(QtGui.QIcon(gui_setup.image1_path))

    def check_login(self):
        username = self.username.text()
        password = self.password.text()

        # Implement your login logic here
        # Example code to send login request to a server
        url = "http://25.15.71.9:5000/authenticate_user"
        payload = {"username": username, "password": password}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if response_data.get("message") == "Authentication successful":
            self.message_label.setText("Login successful")
            self.message_label.setStyleSheet("font-size: 14px; color: green;")
            QtCore.QTimer.singleShot(2000, self.show_loading_screen)
        else:
            self.message_label.setText("Incorrect username or password")
            self.message_label.setStyleSheet("font-size: 14px; color: red;")

    def show_loading_screen(self):
        self.loading_screen = LoadingScreen()
        self.loading_screen.show()
        QtCore.QTimer.singleShot(5000, self.load_main_window)

    def load_main_window(self):
        self.loading_screen.close()
        self.clear_window()
        self.showMaximized()

    def clear_window(self):
        # Clear existing layout
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout(central_widget)

        # Add new content here for the main application window after successful login
        self.label_title = QtWidgets.QLabel("Main Dashboard", self)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(self.label_title)

        self.add_dashboard_buttons(main_layout)

    def add_dashboard_buttons(self, layout):
        # Messaging Section
        self.add_dashboard_section(layout, "Messaging", "Send and receive messages.", "#4CAF50")

        # Projects Section
        self.add_dashboard_section(layout, "Projects", "Manage your projects.", "#2196F3")

        # Tasks Section
        self.add_dashboard_section(layout, "Tasks", "Track your tasks.", "#FFC107")

        # Templates Section
        self.add_dashboard_section(layout, "Templates", "Use and manage templates.", "#9C27B0")

    def add_dashboard_section(self, layout, title, description, color):
        section_widget = QtWidgets.QWidget(self)
        section_layout = QtWidgets.QVBoxLayout(section_widget)
        
        button = QtWidgets.QPushButton(title, self)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {color};
                opacity: 0.8;
            }}
        """)
        section_layout.addWidget(button)

        label = QtWidgets.QLabel(description, self)
        label.setStyleSheet("font-size: 14px;")
        section_layout.addWidget(label)

        layout.addWidget(section_widget)

    def create_account(self):
        username = self.username.text()
        password = self.password.text()
        # Implement your account creation logic here
        # Example code to send account creation request to a server
        url = "http://25.15.71.9:5000/create_user"
        payload = {
            "username": username,
            "password": password,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if response_data.get("created"):
            self.message_label.setText("Account created successfully")
            self.message_label.setStyleSheet("font-size: 14px; color: green;")
        else:
            self.message_label.setText("Failed to create account")
            self.message_label.setStyleSheet("font-size: 14px; color: red;")

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(
            QtWidgets.QApplication.desktop().cursor().pos()
        )
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

class LoadingScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Loading")
        self.setGeometry(100, 100, 300, 100)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white; border: 2px solid #4CAF50; border-radius: 10px;")

        layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("Loading, please wait", self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.label)

        self.dots = ""
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_loading_text)
        self.timer.start(1000)

        # Center the loading screen
        self.center()

    def update_loading_text(self):
        if self.dots == "...":
            self.dots = ""
        else:
            self.dots += "."
        self.label.setText(f"Loading, please wait{self.dots}")

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(
            QtWidgets.QApplication.desktop().cursor().pos()
        )
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
