from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QFrame, QGridLayout)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class DashboardView(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

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

        # Stats cards
        stats_layout = QGridLayout()
        stats_layout.setSpacing(20)

        stats_data = [
            ("Total Employees", "150", "👥"),
            ("Average Salary", "$5,200", "💰"),
            ("Total Departments", "8", "🏢"),
            ("Active Projects", "12", "📊")
        ]

        for i, (title, value, icon) in enumerate(stats_data):
            card = self.create_stat_card(title, value, icon)
            stats_layout.addWidget(card, i // 2, i % 2)

        layout.addLayout(stats_layout)

        # Charts
        charts_layout = QHBoxLayout()
        
        # Salary Distribution Chart
        salary_chart = self.create_salary_chart()
        charts_layout.addWidget(salary_chart)

        # Department Distribution Chart
        dept_chart = self.create_department_chart()
        charts_layout.addWidget(dept_chart)

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

        fig, ax = plt.subplots()
        salaries = np.random.normal(5000, 1000, 150)
        ax.hist(salaries, bins=30, color='#4299e1')
        ax.set_xlabel('Salary Range')
        ax.set_ylabel('Number of Employees')
        
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        
        return frame

    def create_department_chart(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(frame)
        
        title = QLabel("Department Distribution")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2d3748;")
        layout.addWidget(title)

        fig, ax = plt.subplots()
        departments = ['IT', 'HR', 'Sales', 'Marketing', 'Finance']
        sizes = [30, 20, 35, 25, 40]
        ax.pie(sizes, labels=departments, autopct='%1.1f%%')
        
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        
        return frame
