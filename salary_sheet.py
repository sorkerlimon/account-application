from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                           QTableWidgetItem, QPushButton, QHeaderView,
                           QMessageBox, QMenu, QFrame, QDialog, QFormLayout,
                           QLineEdit, QDateEdit, QLabel, QComboBox)
from PyQt6.QtCore import Qt, QDate, QDateTime
from PyQt6.QtGui import QColor, QIcon, QFont, QAction
from mysql.connector import Error
from db import get_db_connection

class SalarySheet(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header section
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Salary Sheet")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1e293b;
        """)
        header_layout.addWidget(title)

        # Add New Salary Button
        new_salary_btn = QPushButton("+ New Salary")
        new_salary_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        new_salary_btn.clicked.connect(self.show_salary_dialog)
        header_layout.addWidget(new_salary_btn)
        layout.addWidget(header)

        # Table
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                gridline-color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #e2e8f0;
                font-weight: bold;
                color: #1e293b;
            }
        """)
        layout.addWidget(self.table)
        self.setup_table()

    def setup_table(self):
        headers = ["ID", "Employee", "Base Salary", "Bonus", "Payment Date", "Status", "Created At", "Actions"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Set row and header heights
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.horizontalHeader().setFixedHeight(50)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(True)

        # Make table responsive
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)

        # Set column widths
        column_widths = {
            0: 60,   # ID
            1: 200,  # Employee
            2: 120,  # Base Salary
            3: 100,  # Bonus
            4: 120,  # Payment Date
            5: 100,  # Status
            6: 120,  # Created At
            7: 100   # Actions
        }

        for col, width in column_widths.items():
            self.table.setColumnWidth(col, width)

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            query = """
                SELECT s.salary_id, CONCAT(e.first_name, ' ', e.last_name) as employee_name,
                       s.base_salary, s.bonus, s.payment_date, s.payment_status, s.created_at
                FROM salaries s
                JOIN employees e ON s.employee_id = e.employee_id
                ORDER BY s.salary_id DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            self.table.setRowCount(len(rows))

            for row_idx, row_data in enumerate(rows):
                bg_color = "#f8fafc" if row_idx % 2 else "white"

                for col, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setBackground(QColor(bg_color))

                    # Format currency for salary and bonus
                    if col in [2, 3]:  # base_salary and bonus columns
                        item.setText(f"${value:,.2f}")
                    
                    # Format dates
                    elif col in [4, 6]:  # payment_date and created_at
                        if isinstance(value, str):
                            item.setText(value)
                        else:
                            item.setText(value.strftime("%Y-%m-%d"))
                    
                    # Color code status
                    elif col == 5:  # status column
                        if value.lower() == "paid":
                            item.setForeground(QColor("#22c55e"))
                        else:
                            item.setForeground(QColor("#ef4444"))

                    self.table.setItem(row_idx, col, item)

                # Add action buttons
                action_widget = self.create_action_widget(row_idx)
                self.table.setCellWidget(row_idx, len(row_data), action_widget)

            cursor.close()
            connection.close()

        except Error as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to fetch salary data: {str(e)}",
                QMessageBox.StandardButton.Ok
            )

    def create_action_widget(self, row):
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(0)

        action_btn = QPushButton("⋮")
        action_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #64748b;
                border: none;
                padding: 0px;
                font-size: 20px;
                font-weight: bold;
                min-width: 24px;
                max-width: 24px;
                min-height: 24px;
                max-height: 24px;
                text-align: center;
                line-height: 24px;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
                border-radius: 4px;
            }
        """)
        action_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 0px;
            }
            QMenu::item {
                padding: 8px 24px;
                font-size: 14px;
            }
            QMenu::item:selected {
                background-color: #f1f5f9;
                color: #1e293b;
            }
        """)

        edit_action = QAction("✎ Edit", self)
        delete_action = QAction("🗑 Delete", self)
        mark_paid_action = QAction("✓ Mark as Paid", self)

        edit_action.triggered.connect(lambda checked, r=row: self.edit_salary(r))
        delete_action.triggered.connect(lambda checked, r=row: self.delete_salary(r))
        mark_paid_action.triggered.connect(lambda checked, r=row: self.mark_as_paid(r))

        menu.addAction(edit_action)
        menu.addAction(mark_paid_action)
        menu.addAction(delete_action)

        action_btn.clicked.connect(lambda checked, b=action_btn, m=menu: self.show_action_menu(b, m))

        action_layout.addStretch()
        action_layout.addWidget(action_btn)
        action_layout.addStretch()

        return action_widget

    def show_action_menu(self, button, menu):
        pos = button.mapToGlobal(button.rect().bottomLeft())
        menu.exec(pos)

    def save_salary(self, employee_id, base_salary, bonus, payment_date, status, salary_id=None):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            if salary_id:  # Update existing salary
                query = """
                    UPDATE salaries 
                    SET employee_id = %s, base_salary = %s, bonus = %s,
                        payment_date = %s, payment_status = %s
                    WHERE salary_id = %s
                """
                cursor.execute(query, (employee_id, base_salary, bonus, 
                                    payment_date, status, salary_id))
            else:  # Insert new salary
                query = """
                    INSERT INTO salaries 
                    (employee_id, base_salary, bonus, payment_date, payment_status)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (employee_id, base_salary, bonus, 
                                    payment_date, status))

            connection.commit()
            cursor.close()
            connection.close()
            return True

        except Error as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save salary: {str(e)}",
                QMessageBox.StandardButton.Ok
            )
            return False

    def show_salary_dialog(self, salary_data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Salary" if not salary_data else "Edit Salary")
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #1e293b;
                font-weight: 500;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                background: white;
                min-width: 250px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton[type="submit"] {
                background-color: #3b82f6;
                color: white;
                border: none;
            }
            QPushButton[type="submit"]:hover {
                background-color: #2563eb;
            }
            QPushButton[type="cancel"] {
                background-color: #e2e8f0;
                color: #1e293b;
                border: none;
            }
            QPushButton[type="cancel"]:hover {
                background-color: #cbd5e1;
            }
        """)

        layout = QFormLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Employee selection
        employee_combo = QComboBox()
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT employee_id, CONCAT(first_name, ' ', last_name) FROM employees")
            employees = cursor.fetchall()
            for emp_id, name in employees:
                employee_combo.addItem(name, emp_id)
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error fetching employees: {e}")

        # Base salary and bonus fields
        base_salary_input = QLineEdit()
        base_salary_input.setPlaceholderText("Enter base salary")
        bonus_input = QLineEdit()
        bonus_input.setPlaceholderText("Enter bonus (optional)")

        # Payment date
        payment_date = QDateEdit()
        payment_date.setCalendarPopup(True)
        payment_date.setDate(QDate.currentDate())

        # Status selection
        status_combo = QComboBox()
        status_combo.addItems(["pending", "paid"])

        # Add fields to layout
        layout.addRow("Employee:", employee_combo)
        layout.addRow("Base Salary:", base_salary_input)
        layout.addRow("Bonus:", bonus_input)
        layout.addRow("Payment Date:", payment_date)
        layout.addRow("Status:", status_combo)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setProperty("type", "submit")
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setProperty("type", "cancel")

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addRow("", button_layout)

        # Set values if editing
        if salary_data:
            employee_combo.setCurrentText(salary_data['employee'])
            base_salary_input.setText(str(salary_data['base_salary']))
            bonus_input.setText(str(salary_data['bonus']))
            payment_date.setDate(QDate.fromString(salary_data['payment_date'], "yyyy-MM-dd"))
            status_combo.setCurrentText(salary_data['status'])

        def save():
            try:
                employee_id = employee_combo.currentData()
                base_salary = float(base_salary_input.text())
                bonus = float(bonus_input.text() or 0)
                payment_date_str = payment_date.date().toString("yyyy-MM-dd")
                status = status_combo.currentText()

                if salary_data:
                    success = self.save_salary(employee_id, base_salary, bonus, 
                                            payment_date_str, status, salary_data['id'])
                else:
                    success = self.save_salary(employee_id, base_salary, bonus, 
                                            payment_date_str, status)

                if success:
                    dialog.accept()
                    self.setup_table()
                    self.show_success_message("Salary saved successfully!")

            except ValueError:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Please enter valid numbers for salary and bonus.",
                    QMessageBox.StandardButton.Ok
                )

        save_btn.clicked.connect(save)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec()

    def edit_salary(self, row):
        salary_data = {
            'id': int(self.table.item(row, 0).text()),
            'employee': self.table.item(row, 1).text(),
            'base_salary': float(self.table.item(row, 2).text().replace('$', '').replace(',', '')),
            'bonus': float(self.table.item(row, 3).text().replace('$', '').replace(',', '')),
            'payment_date': self.table.item(row, 4).text(),
            'status': self.table.item(row, 5).text()
        }
        self.show_salary_dialog(salary_data)

    def delete_salary(self, row):
        try:
            salary_id = int(self.table.item(row, 0).text())
            employee_name = self.table.item(row, 1).text()

            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete salary record for {employee_name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                connection = get_db_connection()
                cursor = connection.cursor()

                query = "DELETE FROM salaries WHERE salary_id = %s"
                cursor.execute(query, (salary_id,))
                connection.commit()

                cursor.close()
                connection.close()

                self.show_success_message("Salary record deleted successfully!")
                self.setup_table()

        except Error as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to delete salary record: {str(e)}",
                QMessageBox.StandardButton.Ok
            )

    def mark_as_paid(self, row):
        try:
            salary_id = int(self.table.item(row, 0).text())
            employee_name = self.table.item(row, 1).text()

            connection = get_db_connection()
            cursor = connection.cursor()

            query = "UPDATE salaries SET payment_status = 'paid' WHERE salary_id = %s"
            cursor.execute(query, (salary_id,))
            connection.commit()

            cursor.close()
            connection.close()

            self.show_success_message(f"Salary marked as paid for {employee_name}")
            self.setup_table()

        except Error as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to update status: {str(e)}",
                QMessageBox.StandardButton.Ok
            )

    def show_success_message(self, message):
        msg = QMessageBox(self)
        msg.setWindowTitle("Success")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #1e293b;
                min-width: 300px;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        msg.exec()
