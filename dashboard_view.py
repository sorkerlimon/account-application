from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QFrame, QGridLayout)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from db import get_db_connection

class DashboardView(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.conn = get_db_connection()
        self.init_ui()

    def get_dashboard_data(self):
        try:
            cursor = self.conn.cursor()
            
            # Get total employees
            cursor.execute("SELECT COUNT(*) as count FROM employees WHERE status = 'active'")
            total_employees = cursor.fetchone()[0]
            
            # Get average salary
            cursor.execute("""
                SELECT COALESCE(AVG(base_salary + COALESCE(bonus, 0)), 0) as avg_salary 
                FROM salaries s 
                JOIN employees e ON s.employee_id = e.employee_id 
                WHERE e.status = 'active'
            """)
            avg_salary = cursor.fetchone()[0]
            
            cursor.close()
            return {
                'total_employees': total_employees,
                'avg_salary': avg_salary
            }
        except Exception as e:
            print(f"Error fetching dashboard data: {e}")
            return {
                'total_employees': 0,
                'avg_salary': 0
            }

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        header = QLabel("Dashboard Overview")
        header.setStyleSheet("""
            font-size: 24px;
            color: #1a202c;
            font-weight: bold;
            margin-bottom: 20px;
        """)
        layout.addWidget(header)

        # Get real data from database
        dashboard_data = self.get_dashboard_data()

        # Stats cards
        stats_layout = QGridLayout()
        stats_layout.setSpacing(20)

        stats_data = [
            ("Total Employees", str(dashboard_data['total_employees']), "👥"),
            ("Average Salary", f"${dashboard_data['avg_salary']:,.2f}", "💰"),
        ]

        for i, (title, value, icon) in enumerate(stats_data):
            card = self.create_stat_card(title, value, icon)
            stats_layout.addWidget(card, 0, i)

        layout.addLayout(stats_layout)

        # Charts
        charts_layout = QHBoxLayout()
        
        # Salary Distribution Chart
        salary_chart = self.create_salary_chart()
        charts_layout.addWidget(salary_chart)

        # Invoice Status Chart
        invoice_chart = self.create_invoice_chart()
        charts_layout.addWidget(invoice_chart)

        layout.addLayout(charts_layout)
        layout.addStretch()

    def create_stat_card(self, title, value, icon):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        card_layout = QVBoxLayout(card)

        # Icon and title
        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #4a5568; font-size: 16px;")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        card_layout.addLayout(header_layout)

        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2d3748;")
        card_layout.addWidget(value_label)

        return card

    def create_salary_chart(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(frame)
        
        title = QLabel("Salary Distribution")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2d3748;")
        layout.addWidget(title)

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT base_salary + COALESCE(bonus, 0) as total_salary 
                FROM salaries s 
                JOIN employees e ON s.employee_id = e.employee_id 
                WHERE e.status = 'active'
            """)
            salary_data = cursor.fetchall()
            cursor.close()
            
            salaries = [row[0] for row in salary_data]

            fig, ax = plt.subplots()
            if salaries:
                ax.hist(salaries, bins=min(30, len(salaries)), color='#4299e1')
                ax.set_xlabel('Salary Range ($)')
                ax.set_ylabel('Number of Employees')
            else:
                ax.text(0.5, 0.5, 'No salary data available', 
                       horizontalalignment='center', verticalalignment='center')
            
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)
            
        except Exception as e:
            print(f"Error creating salary chart: {e}")
            error_label = QLabel("Error loading salary data")
            error_label.setStyleSheet("color: #e53e3e;")
            layout.addWidget(error_label)
        
        return frame

    def create_invoice_chart(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(frame)
        
        title = QLabel("Invoice Status Distribution")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2d3748;")
        layout.addWidget(title)

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM invoices 
                GROUP BY status
            """)
            invoice_data = cursor.fetchall()
            cursor.close()
            
            statuses = [row[0] for row in invoice_data]
            counts = [row[1] for row in invoice_data]

            fig, ax = plt.subplots()
            if invoice_data:
                colors = ['#4299e1', '#48bb78', '#ecc94b', '#f56565']  # blue, green, yellow, red
                ax.pie(counts, labels=statuses, autopct='%1.1f%%', colors=colors)
            else:
                ax.text(0.5, 0.5, 'No invoice data available', 
                       horizontalalignment='center', verticalalignment='center')
            
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)
            
        except Exception as e:
            print(f"Error creating invoice chart: {e}")
            error_label = QLabel("Error loading invoice data")
            error_label.setStyleSheet("color: #e53e3e;")
            layout.addWidget(error_label)
        
        return frame

    def closeEvent(self, event):
        # Clean up matplotlib figures when the widget is closed
        plt.close('all')
        event.accept()
