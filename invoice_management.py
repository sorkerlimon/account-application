from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFrame, QTableWidget, QTableWidgetItem,
                           QComboBox, QCalendarWidget, QMenu, QHeaderView,
                           QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from invoice_generator import InvoiceViewer
from db import (get_employees, get_invoices, create_invoice, 
               update_invoice_status, get_employee_salary)
from datetime import datetime, timedelta
from email_utils import send_invoice_email
import os

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
        self.employee_combo = QComboBox()
        self.employee_combo.setObjectName("employee_combo")
        
        # Load employees from database
        self.employees = get_employees()
        for employee in self.employees:
            self.employee_combo.addItem(employee['full_name'], employee['employee_id'])
            
        self.employee_combo.setStyleSheet("""
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
        employee_group.addWidget(self.employee_combo)
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
        headers = ["Invoice ID", "Employee", "Email", "Month", "Year", "Amount", "Bonus", "Status", "Actions"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set row and header heights
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.horizontalHeader().setFixedHeight(50)
        self.table.verticalHeader().setVisible(False)
        
        # Disable selection
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
        # Get data from database
        invoices = get_invoices()
        self.table.setRowCount(len(invoices))
        
        for row, invoice in enumerate(invoices):
            bg_color = "#f8fafc" if row % 2 else "white"
            
            # Extract month and year from issue_date
            issue_date = invoice['issue_date']
            month = issue_date.strftime("%B")
            year = issue_date.strftime("%Y")
            
            # Format amount and bonus with currency symbol
            amount = f"${invoice['amount']:,.2f}"
            bonus = f"${invoice['bonus']:,.2f}" if invoice['bonus'] else "$0.00"
            
            # Add data to cells
            data = [
                invoice['invoice_number'],
                invoice['employee_name'],
                invoice['employee_email'],
                month,
                year,
                amount,
                bonus
            ]
            
            for col, text in enumerate(data):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                # Store invoice_id as item data for later use
                if col == 0:
                    item.setData(Qt.ItemDataRole.UserRole, invoice['invoice_id'])
                self.table.setItem(row, col, item)
                item.setBackground(QColor(bg_color))
            
            # Status label
            status_widget = QWidget()
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(8, 0, 8, 0)
            status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            status = invoice['status'].capitalize()
            status_label = QLabel(status)
            status_color = '#22c55e' if status == 'Paid' else '#f97316'
            status_label.setStyleSheet(f"""
                QLabel {{
                    color: white;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-weight: 500;
                    background-color: {status_color};
                }}
            """)
            status_layout.addWidget(status_label)
            self.table.setCellWidget(row, 7, status_widget)
            
            # Actions column
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
            send_action = menu.addAction("📧 Send Email")
            if status == "Draft":
                mark_paid_action = menu.addAction("✓ Mark as Paid")
                mark_paid_action.triggered.connect(lambda checked, r=row: self.mark_as_paid(r))
            
            # Connect actions
            view_action.triggered.connect(lambda checked, r=row: self.show_invoice_viewer(r))
            download_action.triggered.connect(lambda checked, r=row: self.download_invoice(r))
            send_action.triggered.connect(lambda checked, r=row: self.send_invoice_email(r))
            action_btn.clicked.connect(lambda checked, b=action_btn, m=menu: self.show_action_menu(b, m))
            
            actions_layout.addWidget(action_btn)
            self.table.setCellWidget(row, 8, actions_widget)

        # Make columns responsive
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 120)  # Invoice ID
        
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Employee
        
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Email
        
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 120)  # Month
        
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 100)  # Year
        
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(5, 120)  # Amount
        
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(6, 100)  # Bonus
        
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(7, 120)  # Status
        
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(8, 100)  # Actions

        # Make table stretch to fill the frame
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def show_invoice_viewer(self, row):
        invoice_data = {
            'id': self.table.item(row, 0).text(),
            'employee': self.table.item(row, 1).text(),
            'month': self.table.item(row, 3).text(),
            'year': self.table.item(row, 4).text(),
            'amount': self.table.item(row, 5).text(),
            'bonus': self.table.item(row, 6).text(),
            'status': self.table.cellWidget(row, 7).findChild(QLabel).text()
        }
        viewer = InvoiceViewer(invoice_data, self)
        viewer.exec()

    def show_action_menu(self, button, menu):
        """Show the action menu below the button"""
        pos = button.mapToGlobal(button.rect().bottomLeft())
        menu.exec(pos)

    def generate_new_invoice(self):
        # Get selected employee
        employee_id = self.employee_combo.currentData()
        if not employee_id:
            QMessageBox.warning(
                self,
                "Error",
                "No employee selected",
                QMessageBox.StandardButton.Ok
            )
            return
            
        # Get selected month and year
        month = self.findChild(QFrame, "date_picker").month_combo.currentText()
        year = int(self.findChild(QFrame, "date_picker").year_combo.currentText())
        
        # Convert month name to number (1-12)
        month_num = datetime.strptime(month, "%B").month
        
        # Create issue date and due date
        issue_date = datetime(year, month_num, 1)  # First day of month
        due_date = issue_date + timedelta(days=30)  # Due in 30 days
        
        # Get employee's salary information
        salary_info = get_employee_salary(employee_id)
        if not salary_info:
            QMessageBox.warning(
                self,
                "No Salary Information",
                f"No salary information found for this employee. Please set up the salary first.",
                QMessageBox.StandardButton.Ok
            )
            return
            
        # Create new invoice
        invoice_id = create_invoice(
            employee_id=employee_id,
            amount=salary_info['base_salary'],
            issue_date=issue_date,
            due_date=due_date
        )
        
        if invoice_id:
            # Refresh the table to show new data
            self.setup_table()
            QMessageBox.information(
                self,
                "Success",
                "Invoice generated successfully!",
                QMessageBox.StandardButton.Ok
            )
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Failed to create invoice. Please try again.",
                QMessageBox.StandardButton.Ok
            )

    def download_invoice(self, row):
        """Helper method to download invoice directly"""
        invoice_data = {
            'id': self.table.item(row, 0).text(),
            'employee': self.table.item(row, 1).text(),
            'month': self.table.item(row, 3).text(),
            'year': self.table.item(row, 4).text(),
            'amount': self.table.item(row, 5).text(),
            'bonus': self.table.item(row, 6).text(),
            'status': self.table.cellWidget(row, 7).findChild(QLabel).text()
        }
        
        # Create temporary viewer to use its PDF generation
        viewer = InvoiceViewer(invoice_data, self)
        return viewer.generate_pdf()  # Return the PDF path

    def send_invoice_email(self, row):
        """Send invoice via email"""
        invoice_number = self.table.item(row, 0).text()
        recipient_email = self.table.item(row, 2).text()
        
        # First generate/download the PDF
        invoice_data = {
            'id': invoice_number,
            'employee': self.table.item(row, 1).text(),
            'month': self.table.item(row, 3).text(),
            'year': self.table.item(row, 4).text(),
            'amount': self.table.item(row, 5).text(),
            'bonus': self.table.item(row, 6).text(),
            'status': self.table.cellWidget(row, 7).findChild(QLabel).text()
        }
        
        # Create temporary viewer to generate PDF without showing save dialog
        viewer = InvoiceViewer(invoice_data, None)
        pdf_path = viewer.generate_pdf(show_save_dialog=False)
        
        if pdf_path and os.path.exists(pdf_path):
            # Send email
            if send_invoice_email(recipient_email, invoice_number, pdf_path):
                QMessageBox.information(
                    self,
                    "Success",
                    f"Invoice has been sent to {recipient_email}",
                    QMessageBox.StandardButton.Ok
                )
                # Clean up the temporary PDF file
                try:
                    os.remove(pdf_path)
                except:
                    pass
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Failed to send email. Please check your email settings and try again.",
                    QMessageBox.StandardButton.Ok
                )
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Failed to generate PDF. Please try again.",
                QMessageBox.StandardButton.Ok
            )

    def mark_as_paid(self, row):
        """Update invoice status from Draft to Paid"""
        invoice_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        if update_invoice_status(invoice_id, 'paid'):
            # Update the UI
            self.setup_table()
