import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QFrame, QScrollArea, QTabWidget,
                           QLineEdit, QTableWidget, QTableWidgetItem, QComboBox,
                           QDateEdit, QSpinBox, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime

class DashboardWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        # Sample data - replace with real data in production
        self.employees = [
            {"id": 1, "name": "John Doe", "salary": 5000, "department": "IT"},
            {"id": 2, "name": "Jane Smith", "salary": 6000, "department": "HR"},
            {"id": 3, "name": "Bob Johnson", "salary": 4500, "department": "Finance"},
            {"id": 4, "name": "Alice Brown", "salary": 5500, "department": "Marketing"},
        ]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Employee Management Dashboard")
        self.setFixedSize(1400, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QTabWidget::pane {
                border: none;
                background-color: #f0f2f5;
            }
            QTabBar::tab {
                background-color: #ffffff;
                color: #333333;
                padding: 12px 30px;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #1a237e;
                color: white;
            }
        """)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create top bar
        self.create_top_bar()

        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("QTabWidget::pane { padding: 20px; }")
        
        # Add tabs
        tab_widget.addTab(self.create_dashboard_tab(), "Dashboard")
        tab_widget.addTab(self.create_salary_tab(), "Salary Management")
        tab_widget.addTab(self.create_invoice_tab(), "Invoice Generation")

        main_layout.addWidget(tab_widget)

    def create_dashboard_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)

        # Top stats cards
        stats_layout = QHBoxLayout()
        stats_data = [
            ("Total Employees", str(len(self.employees)), "#2196F3"),
            ("Average Salary", f"${self.calculate_average_salary():,.2f}", "#4CAF50"),
            ("Total Payroll", f"${self.calculate_total_payroll():,.2f}", "#FF9800"),
            ("Departments", str(len(set(emp['department'] for emp in self.employees))), "#9C27B0")
        ]
        for title, value, color in stats_data:
            self.create_stat_widget(stats_layout, title, value, color)
        layout.addLayout(stats_layout)

        # Charts section
        charts_layout = QHBoxLayout()
        
        # Salary Distribution Chart
        salary_chart = self.create_salary_distribution_chart()
        charts_layout.addWidget(salary_chart)
        
        # Department Distribution Chart
        dept_chart = self.create_department_distribution_chart()
        charts_layout.addWidget(dept_chart)
        
        layout.addLayout(charts_layout)

        return tab

    def create_salary_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)

        # Employee selection section
        selection_layout = QHBoxLayout()
        
        # Employee dropdown
        employee_combo = QComboBox()
        employee_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                min-width: 200px;
            }
        """)
        for emp in self.employees:
            employee_combo.addItem(emp['name'])
        selection_layout.addWidget(employee_combo)
        
        # Salary input
        salary_input = QSpinBox()
        salary_input.setRange(0, 1000000)
        salary_input.setPrefix("$ ")
        salary_input.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                min-width: 150px;
            }
        """)
        selection_layout.addWidget(salary_input)
        
        # Date selection
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        date_edit.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                min-width: 150px;
            }
        """)
        selection_layout.addWidget(date_edit)
        
        # Update button
        update_btn = QPushButton("Update Salary")
        update_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background-color: #1a237e;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #283593;
            }
        """)
        selection_layout.addWidget(update_btn)
        
        layout.addLayout(selection_layout)

        # Salary history table
        table = QTableWidget()
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 8px;
                border: none;
            }
            QHeaderView::section {
                background-color: #1a237e;
                color: white;
                padding: 8px;
                border: none;
            }
        """)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Employee", "Salary", "Date", "Actions"])
        layout.addWidget(table)

        return tab

    def create_invoice_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)

        # Invoice generation controls
        controls_layout = QHBoxLayout()
        
        # Month selection
        month_combo = QComboBox()
        month_combo.addItems(["January", "February", "March", "April", "May", "June",
                            "July", "August", "September", "October", "November", "December"])
        month_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                min-width: 150px;
            }
        """)
        controls_layout.addWidget(month_combo)
        
        # Employee selection
        employee_combo = QComboBox()
        employee_combo.addItems([emp['name'] for emp in self.employees])
        employee_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                min-width: 200px;
            }
        """)
        controls_layout.addWidget(employee_combo)
        
        # Generate button
        generate_btn = QPushButton("Generate Invoice")
        generate_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background-color: #1a237e;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #283593;
            }
        """)
        controls_layout.addWidget(generate_btn)
        
        # Export buttons
        export_pdf_btn = QPushButton("Export as PDF")
        export_csv_btn = QPushButton("Export as CSV")
        for btn in [export_pdf_btn, export_csv_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
            """)
            controls_layout.addWidget(btn)
        
        layout.addLayout(controls_layout)

        # Invoice preview area
        preview_frame = QFrame()
        preview_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        preview_layout = QVBoxLayout(preview_frame)
        
        # Sample invoice content
        preview_layout.addWidget(QLabel("Invoice Preview"))
        
        layout.addWidget(preview_frame)

        return tab

    def create_stat_widget(self, layout, title, value, color):
        widget = QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 15px;
                border-left: 5px solid {color};
                padding: 20px;
                min-width: 250px;
            }}
        """)
        
        widget_layout = QVBoxLayout(widget)
        widget_layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14))
        title_label.setStyleSheet("color: #666;")
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        
        widget_layout.addWidget(title_label)
        widget_layout.addWidget(value_label)
        layout.addWidget(widget)

    def create_salary_distribution_chart(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(frame)
        
        figure = Figure(figsize=(6, 4))
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        
        salaries = [emp['salary'] for emp in self.employees]
        ax.hist(salaries, bins=10, color='#1a237e', alpha=0.7)
        ax.set_title('Salary Distribution')
        ax.set_xlabel('Salary Range')
        ax.set_ylabel('Number of Employees')
        
        layout.addWidget(canvas)
        return frame

    def create_department_distribution_chart(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(frame)
        
        figure = Figure(figsize=(6, 4))
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        
        dept_count = {}
        for emp in self.employees:
            dept_count[emp['department']] = dept_count.get(emp['department'], 0) + 1
        
        ax.pie(dept_count.values(), labels=dept_count.keys(), autopct='%1.1f%%',
               colors=['#1a237e', '#2196F3', '#4CAF50', '#FF9800'])
        ax.set_title('Department Distribution')
        
        layout.addWidget(canvas)
        return frame

    def calculate_average_salary(self):
        if not self.employees:
            return 0
        return sum(emp['salary'] for emp in self.employees) / len(self.employees)

    def calculate_total_payroll(self):
        return sum(emp['salary'] for emp in self.employees)

    def create_top_bar(self):
        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: white;")
        top_bar.setFixedHeight(80)
        
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(30, 0, 30, 0)

        # Welcome message
        welcome = QLabel(f"Welcome, {self.user_data[1]}")
        welcome.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        welcome.setStyleSheet("color: #1a237e;")
        layout.addWidget(welcome)

        # Add spacer
        layout.addStretch()

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setFixedSize(100, 40)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        self.layout().addWidget(top_bar)

    def logout(self):
        from login import LoginWindow
        self.hide()
        self.login_window = LoginWindow()
        self.login_window.show()
