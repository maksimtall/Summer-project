import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import gui_setup  # Assuming gui_setup provides image1_path and image2_path
import requests


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Summer Project")
        self.setGeometry(
            100, 100, 400, 250
        )  # Increased height to accommodate the "Show Password" button

        # Center the window
        self.center()

        # Central widget and layout
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout(central_widget)

        # Title label
        self.label_title = QtWidgets.QLabel("Welcome!", self)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(self.label_title)

        # Form layout
        form_layout = QtWidgets.QFormLayout()

        # Username
        self.label_username = QtWidgets.QLabel("Username:", self)
        self.label_username.setStyleSheet("font-size: 14px;")
        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Enter your username")
        self.username.setStyleSheet("padding: 5px; font-size: 14px;")
        form_layout.addRow(self.label_username, self.username)

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

        # Attempt to load icons with error handling
        try:
            eye_icon = QtGui.QPixmap(gui_setup.image1_path).scaled(
                30, 30, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
            eye_off_icon = QtGui.QPixmap(gui_setup.image2_path).scaled(
                30, 30, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
            print("Icons loaded successfully.")  # Debug print
        except Exception as e:
            print(f"Error loading icons: {e}")

        self.show_password_button.setIcon(QtGui.QIcon(eye_icon))  # Set the initial icon
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

        form_layout.addRow(self.label_password, password_layout)

        main_layout.addLayout(form_layout)

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

        # Message label
        self.message_label = QtWidgets.QLabel("", self)
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: red;")
        main_layout.addWidget(self.message_label)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(
            QtWidgets.QApplication.desktop().cursor().pos()
        )
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def toggle_password_visibility(self):
        if self.show_password_button.isChecked():
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
            try:
                eye_off_icon = QtGui.QPixmap(gui_setup.image2_path).scaled(
                    270, 340, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
                )
                self.show_password_button.setIcon(
                    QtGui.QIcon(eye_off_icon)
                )  # Change icon to eye-off
            except FileNotFoundError:
                print(
                    "Error: Image file not found. Make sure hide_password.png is in the correct directory."
                )
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)
            try:
                eye_icon = QtGui.QPixmap(gui_setup.image1_path).scaled(
                    270, 340, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
                )
                self.show_password_button.setIcon(
                    QtGui.QIcon(eye_icon)
                )  # Change icon to eye
            except FileNotFoundError:
                print(
                    "Error: Image file not found. Make sure show_password.png is in the correct directory."
                )

    def check_login(self):
        username = self.username.text()
        password = self.password.text()
        url = "http://127.0.0.1:5000/authenticate_user"
        payload = {"username": username, "password": password}
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, json=payload, headers=headers)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
