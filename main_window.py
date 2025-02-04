from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QStackedWidget, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from dashboard_view import DashboardView
from user_management import UserManagement
from invoice_management import InvoiceManagement

class MainWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Employee Management System")
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QPushButton {
                border: none;
                padding: 15px;
                text-align: left;
                border-radius: 5px;
                color: #ffffff;
                background: transparent;
            }
            QPushButton:hover {
                background-color: #2d3748;
            }
            QPushButton[Active=true] {
                background-color: #2d3748;
            }
        """)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create sidebar
        sidebar = QWidget()
        sidebar.setStyleSheet("background-color: #1a202c;")
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Add logo/brand area
        brand_widget = QWidget()
        brand_widget.setStyleSheet("background-color: #2d3748; padding: 20px;")
        brand_layout = QVBoxLayout(brand_widget)
        brand_label = QLabel("EMS")
        brand_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        brand_layout.addWidget(brand_label)
        sidebar_layout.addWidget(brand_widget)

        # Create navigation buttons
        self.nav_buttons = []
        nav_items = [
            ("Dashboard", "📊"),
            ("User Management", "👥"),
            ("Invoice Management", "📄")
        ]

        for text, icon in nav_items:
            btn = QPushButton(f"{icon} {text}")
            btn.setFont(QFont("Segoe UI", 10))
            btn.setFixedHeight(50)
            btn.setProperty("Active", "false")
            self.nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        layout.addWidget(sidebar)

        # Create stacked widget for different pages
        self.stack = QStackedWidget()
        self.stack.addWidget(DashboardView(self.user_data))
        self.stack.addWidget(UserManagement(self.user_data))
        self.stack.addWidget(InvoiceManagement(self.user_data))
        layout.addWidget(self.stack)

        # Connect buttons
        for i, btn in enumerate(self.nav_buttons):
            btn.clicked.connect(lambda checked, index=i: self.switch_page(index))

        # Set initial active button
        self.switch_page(0)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("Active", "true" if i == index else "false")
            btn.setStyleSheet("") # Force style refresh
