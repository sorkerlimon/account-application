from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                              QMessageBox, QHBoxLayout, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from main_window import MainWindow
from db import get_db_connection, close_db_connection
from mysql.connector import Error
import os
import mysql.connector

# Valid credentials
VALID_EMAIL = "1"
VALID_PASSWORD = "1"

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # Keep a reference to the main window
        self.dashboard = None

    def verify_credentials(self, email, password):
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            query = "SELECT user_id, email FROM users WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Error as e:
            print(f"Error verifying credentials: {e}")
            QMessageBox.critical(
                self,
                "Database Error",
                "Could not verify credentials. Please try again.",
                QMessageBox.StandardButton.Ok
            )
            return None

    def init_ui(self):
        self.setWindowTitle("Employee Management System - Login")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
            QLabel {
                color: #1e293b;
            }
            QLineEdit {
                padding: 12px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
                min-width: 300px;
                margin-top: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)

        # Create main widget and layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left side - Brand/Logo
        left_widget = QWidget()
        left_widget.setStyleSheet("""
            background-color: #1e293b;
        """)
        left_widget.setFixedWidth(500)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.setSpacing(10)

        # Logo and branding
        brand_label = QLabel("EMS")
        brand_label.setStyleSheet("""
            font-size: 64px;
            font-weight: bold;
            color: white;
            margin-bottom: 5px;
        """)
        brand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Employee Management System")
        subtitle.setStyleSheet("""
            font-size: 20px;
            color: #94a3b8;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_layout.addStretch()
        left_layout.addWidget(brand_label)
        left_layout.addWidget(subtitle)
        left_layout.addStretch()

        # Right side - Login Form
        right_widget = QWidget()
        right_widget.setStyleSheet("""
            background-color: white;
        """)
        right_layout = QVBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(60, 0, 60, 0)

        # Form container
        form_container = QFrame()
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # Welcome text
        welcome_label = QLabel("WELCOME BACK")
        welcome_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1e293b;
            letter-spacing: 2px;
        """)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Email input
        email_label = QLabel("Email")
        email_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #1e293b;
            padding-left: 5px;
            margin-top: 5px;
        """)
        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter your email")
        self.email.setFixedWidth(400)

        # Password input
        password_label = QLabel("Password")
        password_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #1e293b;
            padding-left: 5px;
            margin-top: 5px;
        """)
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setFixedWidth(400)

        # Login button
        login_btn = QPushButton("Sign In")
        login_btn.setFixedWidth(400)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.clicked.connect(self.login)

        # Hint
        hint_label = QLabel("Hint: admin@admin.com / admin123")
        hint_label.setStyleSheet("""
            color: #94a3b8;
            font-size: 12px;
        """)
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add widgets to form layout
        form_layout.addWidget(welcome_label)
        form_layout.addSpacing(20)
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email)
        form_layout.addSpacing(5)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password)
        form_layout.addSpacing(25)
        form_layout.addWidget(login_btn)
        form_layout.addSpacing(20)
        form_layout.addWidget(hint_label)

        # Add form to right layout
        right_layout.addWidget(form_container)

        # Add both sides to main layout
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

    def login(self):
        email = self.email.text()
        password = self.password.text()
        
        if not email or not password:
            QMessageBox.warning(
                self,
                "Login Failed",
                "Please enter both email and password.",
                QMessageBox.StandardButton.Ok
            )
            return

        user = self.verify_credentials(email, password)
        
        if user:
            # Create tuple of user data with just user_id and email
            user_data = (user['user_id'], email, email)  # Using email as name since we don't have name field
            self.dashboard = MainWindow(user_data)
            self.dashboard.show()
            self.hide()
        else:
            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid email or password. Please try again.",
                QMessageBox.StandardButton.Ok
            )

    def closeEvent(self, event):
        close_db_connection()
        event.accept()