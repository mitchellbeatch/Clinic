import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QMessageBox, QLineEdit, QPushButton, QVBoxLayout, QCheckBox
from ..controller import Controller, InvalidLoginException, check_login

class LoginDialog(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Medical Clinic System - Login")

        # Create label, text box, and placeholder text for username input
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter your username")

        # Create label, text box, and placeholder text for password input
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Mask password input

        # Create submit button
        self.login_button = QPushButton("Submit", self)
        self.login_button.clicked.connect(self.try_login)

        # Create remember password box
        self.remember = False
        self.remember_box = QCheckBox("Remember Password")

        # Layout for login window
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.remember_box)
        layout.addWidget(self.login_button)
        self.setLayout(layout)
        self.setMinimumSize(300, 100)

    def closeEvent(self, event):
        sys.exit()  # Terminate the entire application

    # Function to run login and handle exceptions
    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            # Allow access if credentials are correct
            if self.controller.login(username, password):
                self.accept()
        except InvalidLoginException:
            # Provide error message when credentials are incorrect
            msg = QMessageBox()
            msg.setText("Login Failed")
            msg.setInformativeText("Incorrect username or password. Please try again.")
            msg.setWindowTitle("Login Error")
            msg.exec()