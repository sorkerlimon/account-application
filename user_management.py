from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFrame, QTableWidget, QTableWidgetItem,
                           QDialog, QFormLayout, QLineEdit, QDateEdit, QHeaderView,
                           QMessageBox, QMenu)
from PyQt6.QtCore import Qt, QDate, QDateTime
from PyQt6.QtGui import QColor, QIcon, QFont

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
        add_btn.clicked.connect(self.show_add_user_dialog)
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
        # Define all columns
        headers = [
            "ID", "First Name", "Last Name", "Email", "Phone", 
            "Hire Date", "Status", "Created At", "Actions"
        ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set row and header heights
        self.table.verticalHeader().setDefaultSectionSize(60)  # Increased row height
        self.table.horizontalHeader().setFixedHeight(50)  # Fixed header height
        self.table.verticalHeader().setVisible(False)  # Hide row numbers
        self.table.setShowGrid(True)  # Show grid lines
        
        # Disable selection
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

        # Sample data
        data = [
            ("1", "John", "Doe", "john@example.com", "+1234567890", 
             "2024-01-15", "Active", "2024-01-15 09:00:00"),
            ("2", "Jane", "Smith", "jane@example.com", "+1234567891", 
             "2024-01-20", "Active", "2024-01-20 10:30:00"),
            ("3", "Bob", "Johnson", "bob@example.com", "+1234567892", 
             "2024-02-01", "Active", "2024-02-01 11:45:00")
        ]

        self.table.setRowCount(len(data))

        for row, user in enumerate(data):
            bg_color = "#f8fafc" if row % 2 else "white"

            # Add data to cells
            for col, text in enumerate(user):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)
                item.setBackground(QColor(bg_color))

            # Status cell with color
            status = self.table.item(row, 6)
            if status.text() == "Active":
                status.setForeground(QColor("#22c55e"))
            else:
                status.setForeground(QColor("#ef4444"))

            # Actions column
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(0)
            
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
            
            # Create menu for actions
            menu = QMenu(self)
            menu.setStyleSheet("""
                QMenu {
                    background-color: white;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 8px 0px;
                    min-width: 160px;
                }
                QMenu::item {
                    padding: 12px 24px;
                    font-size: 14px;
                }
                QMenu::item:selected {
                    background-color: #f1f5f9;
                    color: #1e293b;
                }
            """)
            
            edit_action = menu.addAction("✎ Edit")
            delete_action = menu.addAction("🗑 Delete")
            
            edit_action.triggered.connect(lambda checked, r=row: self.edit_user(r))
            delete_action.triggered.connect(lambda checked, r=row: self.delete_user(r))
            action_btn.clicked.connect(lambda checked, b=action_btn, m=menu: self.show_action_menu(b, m))
            
            actions_layout.addStretch()
            actions_layout.addWidget(action_btn)
            actions_layout.addStretch()
            
            self.table.setCellWidget(row, len(headers) - 1, actions_widget)

        # Set column widths
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 80)  # ID
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 150)  # First Name
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 150)  # Last Name
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Email
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 150)  # Phone
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(5, 120)  # Hire Date
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(6, 100)  # Status
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(7, 180)  # Created At
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(8, 100)  # Actions

    def show_action_menu(self, button, menu):
        """Show the action menu below the Edit button"""
        pos = button.mapToGlobal(button.rect().bottomLeft())
        menu.exec(pos)

    def edit_user(self, row):
        dialog = self.create_user_dialog("Edit User")
        
        # Pre-fill the form with existing data
        first_name = self.table.item(row, 1).text()
        last_name = self.table.item(row, 2).text()
        email = self.table.item(row, 3).text()
        phone = self.table.item(row, 4).text()
        hire_date = QDate.fromString(self.table.item(row, 5).text(), "yyyy-MM-dd")
        
        # Set existing values
        dialog.findChild(QLineEdit, "first_name").setText(first_name)
        dialog.findChild(QLineEdit, "last_name").setText(last_name)
        dialog.findChild(QLineEdit, "email").setText(email)
        dialog.findChild(QLineEdit, "phone").setText(phone)
        dialog.findChild(QDateEdit, "hire_date").setDate(hire_date)
        
        if dialog.exec():
            # Update the table with new values
            first_name = dialog.findChild(QLineEdit, "first_name").text()
            last_name = dialog.findChild(QLineEdit, "last_name").text()
            email = dialog.findChild(QLineEdit, "email").text()
            phone = dialog.findChild(QLineEdit, "phone").text()
            hire_date = dialog.findChild(QDateEdit, "hire_date").date().toString("yyyy-MM-dd")
            
            # Update cells
            self.table.item(row, 1).setText(first_name)
            self.table.item(row, 2).setText(last_name)
            self.table.item(row, 3).setText(email)
            self.table.item(row, 4).setText(phone)
            self.table.item(row, 5).setText(hire_date)

            # Keep background color consistent
            bg_color = "#f8fafc" if row % 2 else "white"
            for col in range(self.table.columnCount() - 1):  # Exclude actions column
                self.table.item(row, col).setBackground(QColor(bg_color))

    def delete_user(self, row):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Confirm Delete")
        
        # Get user's full name
        first_name = self.table.item(row, 1).text()
        last_name = self.table.item(row, 2).text()
        full_name = f"{first_name} {last_name}"
        
        # Set custom text
        dialog.setText(f"Are you sure you want to delete {full_name}?")
        
        # Set icon
        dialog.setIcon(QMessageBox.Icon.Question)
        
        # Set buttons
        yes_btn = QPushButton("Yes")
        no_btn = QPushButton("No")
        
        dialog.addButton(yes_btn, QMessageBox.ButtonRole.YesRole)
        dialog.addButton(no_btn, QMessageBox.ButtonRole.NoRole)
        dialog.setDefaultButton(no_btn)
        
        # Style the dialog
        dialog.setStyleSheet("""
            QMessageBox {
                background-color: white;
                border-radius: 8px;
            }
            QLabel {
                color: #1e293b;
                font-size: 14px;
                padding: 0px;
            }
            QLabel#qt_msgbox_label {
                min-width: 200px;
                padding: 0px 20px;
            }
            QLabel#qt_msgboxex_icon_label {
                padding: 0px;
                margin-left: 20px;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                color: #0ea5e9;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
            }
        """)
        
        # Set custom icon size
        icon = dialog.findChild(QLabel, "qt_msgboxex_icon_label")
        if icon:
            icon.setFixedSize(32, 32)
        
        # Center the text
        text_label = dialog.findChild(QLabel, "qt_msgbox_label")
        if text_label:
            text_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Execute dialog
        if dialog.exec() == 0:  # Yes clicked
            self.table.removeRow(row)

    def show_add_user_dialog(self):
        dialog = self.create_user_dialog("Add New User")
        
        if dialog.exec():
            # Get values from form
            first_name = dialog.findChild(QLineEdit, "first_name").text()
            last_name = dialog.findChild(QLineEdit, "last_name").text()
            email = dialog.findChild(QLineEdit, "email").text()
            phone = dialog.findChild(QLineEdit, "phone").text()
            hire_date = dialog.findChild(QDateEdit, "hire_date").date().toString("yyyy-MM-dd")
            
            # Get current timestamp for Created At
            current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
            
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Add data to cells
            data = [
                str(row + 1),  # ID
                first_name,
                last_name,
                email,
                phone,
                hire_date,
                "Active",  # Default status
                current_time
            ]
            
            for col, text in enumerate(data):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # Set background color based on row
                bg_color = "#f8fafc" if row % 2 else "white"
                item.setBackground(QColor(bg_color))
                
                # Set status color
                if col == 6:  # Status column
                    item.setForeground(QColor("#22c55e"))
                
                self.table.setItem(row, col, item)
            
            # Actions column for new row
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(0)
            
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
            
            # Create menu for actions
            menu = QMenu(self)
            menu.setStyleSheet("""
                QMenu {
                    background-color: white;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 8px 0px;
                    min-width: 160px;
                }
                QMenu::item {
                    padding: 12px 24px;
                    font-size: 14px;
                }
                QMenu::item:selected {
                    background-color: #f1f5f9;
                    color: #1e293b;
                }
            """)
            
            edit_action = menu.addAction("✎ Edit")
            delete_action = menu.addAction("🗑 Delete")
            
            edit_action.triggered.connect(lambda checked, r=row: self.edit_user(r))
            delete_action.triggered.connect(lambda checked, r=row: self.delete_user(r))
            action_btn.clicked.connect(lambda checked, b=action_btn, m=menu: self.show_action_menu(b, m))
            
            actions_layout.addStretch()
            actions_layout.addWidget(action_btn)
            actions_layout.addStretch()
            
            self.table.setCellWidget(row, len(data), actions_widget)

    def create_user_dialog(self, title):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFixedWidth(400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 8px;
            }
            QLineEdit, QDateEdit {
                border: none;
                border-bottom: 2px solid #e2e8f0;
                padding: 8px 0px;
                font-size: 14px;
                width: 100%;
            }
            QLineEdit:focus, QDateEdit:focus {
                border-bottom: 2px solid #0ea5e9;
            }
            QDateEdit::drop-down {
                border: none;
                width: 20px;
            }
            QDateEdit::down-arrow {
                width: 12px;
                height: 12px;
                margin-right: 4px;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(24, 24, 24, 0)
        layout.setSpacing(24)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1e293b;
            margin-bottom: 8px;
        """)
        layout.addWidget(title_label)

        # Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(24)
        form_layout.setContentsMargins(0, 0, 0, 24)
        
        # Input fields with labels
        fields = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Hire Date", "hire_date")
        ]
        
        for label_text, field_name in fields:
            field_container = QVBoxLayout()
            field_container.setSpacing(8)
            
            label = QLabel(label_text)
            label.setStyleSheet("""
                color: #475569;
                font-size: 13px;
                font-weight: 500;
            """)
            
            if field_name == "hire_date":
                input_widget = QDateEdit()
                input_widget.setDate(QDate.currentDate())
                input_widget.setDisplayFormat("yyyy-MM-dd")
                input_widget.setCalendarPopup(True)
            else:
                input_widget = QLineEdit()
            
            input_widget.setObjectName(field_name)
            input_widget.setFixedHeight(36)
            
            field_container.addWidget(label)
            field_container.addWidget(input_widget)
            form_layout.addLayout(field_container)
        
        layout.addLayout(form_layout)
        
        # Bottom buttons section
        button_container = QFrame()
        button_container.setStyleSheet("""
            QFrame {
                background-color: #f8fafc;
                border-top: 1px solid #e2e8f0;
            }
        """)
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(24, 16, 24, 16)
        button_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(170, 36)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #475569;
                border: none;
                border-radius: 6px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """)
        
        save_btn = QPushButton("Save")
        save_btn.setFixedSize(170, 36)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0ea5e9;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0284c7;
            }
        """)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)
        
        save_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)
        
        return dialog