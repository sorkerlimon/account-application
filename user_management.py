from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                           QTableWidgetItem, QPushButton, QHeaderView,
                           QMessageBox, QMenu, QFrame, QDialog, QFormLayout,
                           QLineEdit, QDateEdit, QLabel)
from PyQt6.QtCore import Qt, QDate, QDateTime
from PyQt6.QtGui import QColor, QIcon, QFont, QAction
from mysql.connector import Error
from db import get_db_connection

class UserManagement(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                font-family: 'Segoe UI', sans-serif;
            }
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
            QLabel {
                color: #1e293b;
            }
            QPushButton {
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 20px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header section with gradient
        header = QFrame()
        header.setStyleSheet("""
            QFrame { 
                padding: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #3b82f6, stop:1 #0ea5e9);
                border: none;
            }
        """)
        
        # Update title style
        title = QLabel("User Management")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            letter-spacing: 1px;
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 10, 15, 10)
        header_layout.addWidget(title)
        
        # Update Add User button
        add_btn = QPushButton("＋ New User")
        add_btn.setFixedWidth(140)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                font-size: 14px;
                border: 2px solid white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self.add_user)
        header_layout.addWidget(add_btn)
        layout.addWidget(header)

        # Table Container
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)

        # User Table
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: #e2e8f0;
                border-radius: 12px;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #f1f5f9;
                padding: 0px 16px;
                border: none;
                font-weight: 600;
                color: #475569;
                font-size: 14px;
                border-bottom: 2px solid #e2e8f0;
                height: 50px;
            }
            QTableWidget::item:selected {
                background-color: #f1f5f9;
                color: #1e293b;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f5f9;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        self.setup_table()
        table_layout.addWidget(self.table)
        layout.addWidget(table_frame)

    def setup_table(self):
        # Define all columns based on actual database structure
        headers = [
            "ID", "First Name", "Last Name", "Email", "Phone", 
            "Position", "Hire Date", "Status", "Created At", "Actions"
        ]
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
            1: 120,  # First Name
            2: 120,  # Last Name
            3: 200,  # Email (stretch)
            4: 120,  # Phone
            5: 120,  # Position
            6: 100,  # Hire Date
            7: 80,   # Status
            8: 120,  # Created At
            9: 80    # Actions
        }
        
        for col, width in column_widths.items():
            self.table.setColumnWidth(col, width)
            if col == 3:  # Make email column stretch
                self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Updated query to match actual table structure
            query = """
                SELECT 
                    employee_id, 
                    first_name, 
                    last_name, 
                    email, 
                    phone,
                    position, 
                    hire_date, 
                    status, 
                    created_at
                FROM employees
                ORDER BY employee_id
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
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    
                    # Set status color
                    if col == 7:  # Status column (updated index)
                        if value and value.lower() == "active":
                            item.setForeground(QColor("#22c55e"))
                        else:
                            item.setForeground(QColor("#ef4444"))
                    
                    self.table.setItem(row_idx, col, item)
                
                # Add action button
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
                
                # Create actions
                edit_action = QAction("✎ Edit", self)
                delete_action = QAction("🗑 Delete", self)
                
                # Connect actions directly
                edit_action.triggered.connect(lambda checked, r=row_idx: self.edit_user(r))
                delete_action.triggered.connect(lambda checked, r=row_idx: self.delete_user(r))
                
                # Add actions to menu
                menu.addAction(edit_action)
                menu.addAction(delete_action)
                
                # Connect button to show menu
                action_btn.clicked.connect(lambda checked, b=action_btn, m=menu: self.show_action_menu(b, m))
                
                action_layout.addStretch()
                action_layout.addWidget(action_btn)
                action_layout.addStretch()
                
                self.table.setCellWidget(row_idx, len(row_data), action_widget)
            
            cursor.close()
            connection.close()
            
        except Error as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to fetch employee data: {str(e)}",
                QMessageBox.StandardButton.Ok
            )

    def show_action_menu(self, button, menu):
        """Show the action menu below the button"""
        pos = button.mapToGlobal(button.rect().bottomLeft())
        menu.exec(pos)

    def delete_user(self, row):
        try:
            # Get user details
            user_id = int(self.table.item(row, 0).text())
            name = f"{self.table.item(row, 1).text()} {self.table.item(row, 2).text()}"
            
            # Show confirmation dialog
            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete {name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Connect to database
                connection = get_db_connection()
                cursor = connection.cursor()
                
                # Execute delete query
                query = "DELETE FROM employees WHERE employee_id = %s"
                cursor.execute(query, (user_id,))
                
                # Commit the transaction
                connection.commit()
                
                # Close database connections
                cursor.close()
                connection.close()
                
                # Show success message
                self.show_success_message("User deleted successfully!")
                
                # Refresh the table
                self.setup_table()
                
        except Error as e:
            print(f"Database Error: {str(e)}")
            QMessageBox.critical(
                self,
                "Database Error",
                f"Failed to delete user: {str(e)}",
                QMessageBox.StandardButton.Ok
            )
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"An unexpected error occurred: {str(e)}",
                QMessageBox.StandardButton.Ok
            )

    def create_user_dialog(self, is_edit=False):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit User" if is_edit else "Add New User")
        dialog.setFixedWidth(400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 14px;
                color: #1e293b;
                font-weight: 500;
            }
            QLineEdit, QDateEdit {
                padding: 8px;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                font-size: 14px;
                min-height: 24px;
            }
            QLineEdit:focus, QDateEdit:focus {
                border: 2px solid #3b82f6;
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
            QPushButton#cancelButton {
                background-color: #e2e8f0;
                color: #1e293b;
            }
            QPushButton#cancelButton:hover {
                background-color: #cbd5e1;
            }
        """)

        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Create input fields
        fields = {
            'first_name': QLineEdit(),
            'last_name': QLineEdit(),
            'email': QLineEdit(),
            'phone': QLineEdit(),
            'position': QLineEdit(),
            'hire_date': QDateEdit()
        }

        # Set object names for later reference
        for name, widget in fields.items():
            widget.setObjectName(name)

        # Configure date field
        fields['hire_date'].setCalendarPopup(True)
        fields['hire_date'].setDate(QDate.currentDate())

        # Add fields to form
        form_layout.addRow("First Name:", fields['first_name'])
        form_layout.addRow("Last Name:", fields['last_name'])
        form_layout.addRow("Email:", fields['email'])
        form_layout.addRow("Phone:", fields['phone'])
        form_layout.addRow("Position:", fields['position'])
        form_layout.addRow("Hire Date:", fields['hire_date'])

        # Add form to main layout
        layout.addLayout(form_layout)

        # Button container
        button_container = QHBoxLayout()
        button_container.setSpacing(10)

        # Create buttons
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("cancelButton")

        # Add buttons to container
        button_container.addWidget(cancel_button)
        button_container.addWidget(save_button)

        # Add button container to main layout
        layout.addSpacing(20)
        layout.addLayout(button_container)

        # Connect buttons
        save_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        return dialog

    def add_user(self):
        dialog = self.create_user_dialog()
        
        if dialog.exec():
            try:
                connection = get_db_connection()
                cursor = connection.cursor()

                # Get values from dialog
                first_name = dialog.findChild(QLineEdit, "first_name").text()
                last_name = dialog.findChild(QLineEdit, "last_name").text()
                email = dialog.findChild(QLineEdit, "email").text()
                phone = dialog.findChild(QLineEdit, "phone").text()
                position = dialog.findChild(QLineEdit, "position").text()
                hire_date = dialog.findChild(QDateEdit, "hire_date").date().toString("yyyy-MM-dd")

                # Insert new user
                query = """
                    INSERT INTO employees (
                        first_name, last_name, email, phone, 
                        position, hire_date, status, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                """
                values = (
                    first_name, last_name, email, phone,
                    position, hire_date, "active"
                )
                
                cursor.execute(query, values)
                connection.commit()
                cursor.close()

                # Refresh table
                self.setup_table()

                self.show_success_message("User added successfully!")

            except Error as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to add user: {str(e)}",
                    QMessageBox.StandardButton.Ok
                )

    def edit_user(self, row):
        dialog = self.create_user_dialog(is_edit=True)
        
        # Get current values
        user_id = self.table.item(row, 0).text()
        first_name = self.table.item(row, 1).text()
        last_name = self.table.item(row, 2).text()
        email = self.table.item(row, 3).text()
        phone = self.table.item(row, 4).text()
        position = self.table.item(row, 5).text()
        hire_date = QDate.fromString(self.table.item(row, 6).text(), "yyyy-MM-dd")
        
        # Set values in dialog
        dialog.findChild(QLineEdit, "first_name").setText(first_name)
        dialog.findChild(QLineEdit, "last_name").setText(last_name)
        dialog.findChild(QLineEdit, "email").setText(email)
        dialog.findChild(QLineEdit, "phone").setText(phone)
        dialog.findChild(QLineEdit, "position").setText(position)
        dialog.findChild(QDateEdit, "hire_date").setDate(hire_date)
        
        if dialog.exec():
            try:
                connection = get_db_connection()
                cursor = connection.cursor()

                # Get updated values
                first_name = dialog.findChild(QLineEdit, "first_name").text()
                last_name = dialog.findChild(QLineEdit, "last_name").text()
                email = dialog.findChild(QLineEdit, "email").text()
                phone = dialog.findChild(QLineEdit, "phone").text()
                position = dialog.findChild(QLineEdit, "position").text()
                hire_date = dialog.findChild(QDateEdit, "hire_date").date().toString("yyyy-MM-dd")

                # Update user
                query = """
                    UPDATE employees SET 
                        first_name = %s,
                        last_name = %s,
                        email = %s,
                        phone = %s,
                        position = %s,
                        hire_date = %s
                    WHERE employee_id = %s
                """
                values = (
                    first_name, last_name, email, phone,
                    position, hire_date, user_id
                )
                
                cursor.execute(query, values)
                connection.commit()
                cursor.close()

                # Refresh table
                self.setup_table()

                self.show_success_message("User updated successfully!")

            except Error as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to update user: {str(e)}",
                    QMessageBox.StandardButton.Ok
                )

    def show_success_message(self, message):
        msg = QMessageBox(self)
        msg.setWindowTitle("Success")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        
        # Create and style OK button
        ok_button = QPushButton("OK")
        msg.addButton(ok_button, QMessageBox.ButtonRole.AcceptRole)
        
        # Style the message box
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                min-width: 420px;
            }
            QLabel {
                color: #1e293b;
                font-size: 14px;
                padding: 20px;
                font-weight: 500;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                min-width: 120px;
                margin: 0px 20px 20px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QLabel#qt_msgbox_label { 
                padding-left: 15px;
            }
            QLabel#qt_msgboxex_icon_label {
                padding: 20px 0px 20px 20px;
            }
        """)
        
        # Set icon size
        icon = msg.findChild(QLabel, "qt_msgboxex_icon_label")
        if icon:
            icon.setFixedSize(40, 40)
        
        msg.exec()