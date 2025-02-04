from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFrame, QTableWidget, QTableWidgetItem,
                           QComboBox, QCalendarWidget, QMenu, QHeaderView)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from invoice_generator import InvoiceViewer

class MonthYearPicker(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        # Month ComboBox
        self.month_combo = QComboBox()
        months = ["January", "February", "March", "April", "May", "June", 
                 "July", "August", "September", "October", "November", "December"]
        self.month_combo.addItems(months)
        current_month = QDate.currentDate().month()
        self.month_combo.setCurrentIndex(current_month - 1)

        # Year ComboBox
        self.year_combo = QComboBox()
        current_year = QDate.currentDate().year()
        years = [str(year) for year in range(current_year - 2, current_year + 3)]
        self.year_combo.addItems(years)
        self.year_combo.setCurrentText(str(current_year))

        # Styling
        self.setStyleSheet("""
            QComboBox {
                padding: 8px 16px;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                background-color: white;
                min-height: 42px;
                font-size: 14px;
                color: #1e293b;
            }
            QComboBox:hover {
                border-color: #cbd5e1;
            }
            QComboBox:focus {
                border: 2px solid #0ea5e9;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox::down-arrow {
                image: url(icons/chevron-down.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px;
                selection-background-color: #f1f5f9;
            }
            QComboBox QAbstractItemView::item {
                min-height: 32px;
                padding: 8px;
                color: #1e293b;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #f1f5f9;
            }
        """)

        self.month_combo.setFixedWidth(160)
        self.year_combo.setFixedWidth(120)

        layout.addWidget(self.month_combo)
        layout.addWidget(self.year_combo)

class InvoiceManagement(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f1f5f9;
                font-family: 'Segoe UI', sans-serif;
            }
            QFrame {
                background-color: white;
                border-radius: 8px;
            }
            QLabel {
                color: #1e293b;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header section
        header = QFrame()
        header.setStyleSheet("QFrame { padding: 15px; }")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 10, 15, 10)

        # Title
        title = QLabel("Invoice Management")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #1e293b;
        """)
        header_layout.addWidget(title)
        layout.addWidget(header)

        # Controls section
        controls = QFrame()
        controls.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #475569;
            }
        """)
        
        controls_layout = QHBoxLayout(controls)
        controls_layout.setSpacing(24)
        controls_layout.setContentsMargins(24, 20, 24, 20)
        
        # Employee selection
        employee_group = QHBoxLayout()
        employee_group.setSpacing(12)
        employee_label = QLabel("Employee:")
        employee_combo = QComboBox()
        employee_combo.setObjectName("employee_combo")
        employee_combo.addItems(["John Doe", "Jane Smith", "Bob Johnson"])
        employee_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 16px;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                background-color: white;
                min-width: 220px;
                min-height: 42px;
                font-size: 14px;
                color: #1e293b;
            }
            QComboBox:hover {
                border-color: #cbd5e1;
            }
            QComboBox:focus {
                border: 2px solid #0ea5e9;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox::down-arrow {
                image: url(icons/chevron-down.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px;
                selection-background-color: #f1f5f9;
            }
        """)
        employee_group.addWidget(employee_label)
        employee_group.addWidget(employee_combo)
        controls_layout.addLayout(employee_group)
        
        # Date picker group
        date_group = QHBoxLayout()
        date_group.setSpacing(12)
        date_label = QLabel("Period:")
        date_picker = MonthYearPicker()
        date_picker.setObjectName("date_picker")
        date_group.addWidget(date_label)
        date_group.addWidget(date_picker)
        controls_layout.addLayout(date_group)
        
        # Generate button
        generate_btn = QPushButton("Generate Invoice")
        generate_btn.setObjectName("generateBtn")
        generate_btn.setStyleSheet("""
            QPushButton#generateBtn {
                background-color: #0ea5e9;
                color: white;
                padding: 8px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                min-height: 42px;
                min-width: 160px;
            }
            QPushButton#generateBtn:hover {
                background-color: #0284c7;
            }
        """)
        generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        generate_btn.clicked.connect(self.generate_new_invoice)
        controls_layout.addWidget(generate_btn)
        
        controls_layout.addStretch()
        layout.addWidget(controls)

        # Table Container
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)

        # Invoice Table
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e2e8f0;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 0px 12px;
                border: none;
                font-weight: bold;
                color: #475569;
                font-size: 14px;
                border-bottom: 2px solid #e2e8f0;
                height: 50px;
            }
            QTableWidget::item:selected {
                background-color: transparent;
                color: #1e293b;
            }
            QTableWidget::item:hover {
                background-color: transparent;
            }
        """)
        
        self.setup_table()
        table_layout.addWidget(self.table)
        layout.addWidget(table_frame)

    def setup_table(self):
        headers = ["Invoice ID", "Employee", "Month", "Year", "Amount", "Bonus", "Status", "Actions"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set row and header heights
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.horizontalHeader().setFixedHeight(50)
        self.table.verticalHeader().setVisible(False)
        
        # Disable selection
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
        # Sample data
        data = [
            ("INV-001", "John Doe", "January", "2024", "$5,000", "$500", "Paid"),
            ("INV-002", "Jane Smith", "January", "2024", "$4,500", "$300", "Pending"),
            ("INV-003", "Bob Johnson", "January", "2024", "$4,800", "$400", "Paid")
        ]
        
        self.table.setRowCount(len(data))
        
        for row, (id_, name, month, year, amount, bonus, status) in enumerate(data):
            bg_color = "#f8fafc" if row % 2 else "white"
            
            # Add data to cells including bonus
            for col, text in enumerate([id_, name, month, year, amount, bonus]):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)
                item.setBackground(QColor(bg_color))
            
            # Status label (now at column 6)
            status_widget = QWidget()
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(8, 0, 8, 0)
            status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            status_label = QLabel(status)
            status_label.setStyleSheet(f"""
                QLabel {{
                    color: white;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-weight: 500;
                    background-color: {('#22c55e' if status == 'Paid' else '#f97316')};
                }}
            """)
            status_layout.addWidget(status_label)
            self.table.setCellWidget(row, 6, status_widget)
            
            # Actions column (now at column 7)
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            action_btn = QPushButton("⋮")
            action_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f1f5f9;
                    color: #1e293b;
                    border: none;
                    border-radius: 4px;
                    padding: 0px;
                    font-size: 24px;
                    font-weight: bold;
                    min-width: 36px;
                    max-width: 36px;
                    min-height: 36px;
                    max-height: 36px;
                    text-align: center;
                    line-height: 36px;
                }
                QPushButton:hover {
                    background-color: #e2e8f0;
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
            
            view_action = menu.addAction("👁 View")
            download_action = menu.addAction("⬇ Download")
            if status == "Pending":
                mark_paid_action = menu.addAction("✓ Mark as Paid")
                mark_paid_action.triggered.connect(lambda checked, r=row: self.mark_as_paid(r))
            
            # Connect actions
            view_action.triggered.connect(lambda checked, r=row: self.show_invoice_viewer(r))
            download_action.triggered.connect(lambda checked, r=row: self.download_invoice(r))
            action_btn.clicked.connect(lambda checked, b=action_btn, m=menu: self.show_action_menu(b, m))
            
            actions_layout.addWidget(action_btn)
            self.table.setCellWidget(row, 7, actions_widget)

        # Make columns responsive
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 120)  # Invoice ID
        
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Employee
        
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 120)  # Month
        
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 100)  # Year
        
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 120)  # Amount
        
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(5, 100)  # Bonus
        
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(6, 120)  # Status
        
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(7, 100)  # Actions

        # Make table stretch to fill the frame
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def show_invoice_viewer(self, row):
        invoice_data = {
            'id': self.table.item(row, 0).text(),
            'employee': self.table.item(row, 1).text(),
            'month': self.table.item(row, 2).text(),
            'year': self.table.item(row, 3).text(),
            'amount': self.table.item(row, 4).text(),
            'bonus': self.table.item(row, 5).text(),
            'status': self.table.cellWidget(row, 6).findChild(QLabel).text()
        }
        viewer = InvoiceViewer(invoice_data, self)
        viewer.exec()

    def show_action_menu(self, button, menu):
        """Show the action menu below the button"""
        pos = button.mapToGlobal(button.rect().bottomLeft())
        menu.exec(pos)

    def generate_new_invoice(self):
        # Get selected values
        employee = self.findChild(QComboBox, "employee_combo").currentText()
        month = self.findChild(QFrame, "date_picker").month_combo.currentText()
        year = self.findChild(QFrame, "date_picker").year_combo.currentText()
        
        # Generate new invoice ID
        last_row = self.table.rowCount()
        new_id = f"INV-{str(last_row + 1).zfill(3)}"
        
        # Sample amount and bonus (you can modify this logic)
        amount = "$5,000"
        bonus = "$500"
        status = "Pending"
        
        # Insert new row
        self.table.insertRow(last_row)
        
        # Add data to cells
        data = [new_id, employee, month, year, amount, bonus]
        for col, text in enumerate(data):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(last_row, col, item)
            
        # Status cell
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(8, 0, 8, 0)
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        status_label = QLabel(status)
        status_label.setStyleSheet("""
            QLabel {
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: 500;
                background-color: #f97316;
            }
        """)
        status_layout.addWidget(status_label)
        self.table.setCellWidget(last_row, 6, status_widget)
        
        # Actions cell
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        action_btn = QPushButton("⋮")
        action_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #1e293b;
                border: none;
                border-radius: 4px;
                padding: 0px;
                font-size: 24px;
                font-weight: bold;
                min-width: 36px;
                max-width: 36px;
                min-height: 36px;
                max-height: 36px;
                text-align: center;
                line-height: 36px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
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
        
        view_action = menu.addAction("👁 View")
        download_action = menu.addAction("⬇ Download")
        mark_paid_action = menu.addAction("✓ Mark as Paid")
        
        # Connect actions
        view_action.triggered.connect(lambda checked, r=last_row: self.show_invoice_viewer(r))
        download_action.triggered.connect(lambda checked, r=last_row: self.download_invoice(r))
        mark_paid_action.triggered.connect(lambda checked, r=last_row: self.mark_as_paid(last_row))
        action_btn.clicked.connect(lambda checked, b=action_btn, m=menu: self.show_action_menu(b, m))
        
        actions_layout.addWidget(action_btn)
        self.table.setCellWidget(last_row, 7, actions_widget)

    def download_invoice(self, row):
        """Helper method to download invoice directly"""
        invoice_data = {
            'id': self.table.item(row, 0).text(),
            'employee': self.table.item(row, 1).text(),
            'month': self.table.item(row, 2).text(),
            'year': self.table.item(row, 3).text(),
            'amount': self.table.item(row, 4).text(),
            'bonus': self.table.item(row, 5).text(),
            'status': self.table.cellWidget(row, 6).findChild(QLabel).text()
        }
        
        # Create temporary viewer to use its PDF generation
        viewer = InvoiceViewer(invoice_data, self)
        viewer.generate_pdf()

    def mark_as_paid(self, row):
        """Update invoice status from Pending to Paid"""
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(8, 0, 8, 0)
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        status_label = QLabel("Paid")
        status_label.setStyleSheet("""
            QLabel {
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: 500;
                background-color: #22c55e;
            }
        """)
        status_layout.addWidget(status_label)
        
        # Update status cell
        self.table.setCellWidget(row, 6, status_widget)
        
        # Update actions menu (remove Mark as Paid option)
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        action_btn = QPushButton("⋮")
        action_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #1e293b;
                border: none;
                border-radius: 4px;
                padding: 0px;
                font-size: 24px;
                font-weight: bold;
                min-width: 36px;
                max-width: 36px;
                min-height: 36px;
                max-height: 36px;
                text-align: center;
                line-height: 36px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """)
        action_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Create new menu without Mark as Paid option
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
        
        view_action = menu.addAction("👁 View")
        download_action = menu.addAction("⬇ Download")
        
        # Connect actions
        view_action.triggered.connect(lambda checked, r=row: self.show_invoice_viewer(r))
        download_action.triggered.connect(lambda checked, r=row: self.download_invoice(r))
        action_btn.clicked.connect(lambda checked, b=action_btn, m=menu: self.show_action_menu(b, m))
        
        actions_layout.addWidget(action_btn)
        self.table.setCellWidget(row, 7, actions_widget)
