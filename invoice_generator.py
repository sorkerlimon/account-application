from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFrame, QWidget, QScrollArea, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import os

class InvoiceViewer(QDialog):
    def __init__(self, invoice_data, parent=None):
        super().__init__(parent)
        self.invoice_data = invoice_data
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Invoice Details")
        self.setMinimumSize(800, 900)
        self.setStyleSheet("""
            QDialog {
                background-color: #f1f5f9;
                font-family: 'Segoe UI', sans-serif;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f1f5f9;
            }
        """)

        # Create container widget for scroll area
        container = QWidget()
        scroll_layout = QVBoxLayout(container)
        scroll_layout.setSpacing(20)

        # Invoice Card
        invoice_card = QFrame()
        invoice_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        card_layout = QVBoxLayout(invoice_card)
        card_layout.setSpacing(20)

        # Header with logo and title
        header = QHBoxLayout()
        company_info = QVBoxLayout()
        
        company_name = QLabel("EMS Company")
        company_name.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1e293b;
        """)
        company_address = QLabel("123 Business Street\nCity, State 12345\nPhone: (555) 123-4567")
        company_address.setStyleSheet("color: #475569;")
        
        company_info.addWidget(company_name)
        company_info.addWidget(company_address)
        header.addLayout(company_info)
        header.addStretch()
        
        # Invoice details on right
        invoice_info = QVBoxLayout()
        invoice_title = QLabel("INVOICE")
        invoice_title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #0ea5e9;
        """)
        invoice_number = QLabel(f"Invoice #: {self.invoice_data['id']}")
        invoice_date = QLabel(f"Date: {self.invoice_data['month']} {self.invoice_data['year']}")
        
        for label in [invoice_number, invoice_date]:
            label.setStyleSheet("""
                color: #475569;
                font-size: 14px;
            """)
        
        invoice_info.addWidget(invoice_title)
        invoice_info.addWidget(invoice_number)
        invoice_info.addWidget(invoice_date)
        header.addLayout(invoice_info)
        
        card_layout.addLayout(header)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #e2e8f0;")
        card_layout.addWidget(separator)

        # Bill to section
        bill_to = QVBoxLayout()
        bill_to_label = QLabel("Bill To:")
        bill_to_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1e293b;
        """)
        employee_name = QLabel(self.invoice_data['employee'])
        employee_name.setStyleSheet("color: #475569;")
        
        bill_to.addWidget(bill_to_label)
        bill_to.addWidget(employee_name)
        card_layout.addLayout(bill_to)

        # Invoice details
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background-color: #f8fafc;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        details_layout = QVBoxLayout(details_frame)

        # Headers
        headers = QHBoxLayout()
        header_style = """
            font-weight: bold;
            color: #1e293b;
            font-size: 14px;
        """
        description_header = QLabel("Description")
        amount_header = QLabel("Amount")
        description_header.setStyleSheet(header_style)
        amount_header.setStyleSheet(header_style)
        
        headers.addWidget(description_header)
        headers.addStretch()
        headers.addWidget(amount_header)
        details_layout.addLayout(headers)

        # Separator
        details_separator = QFrame()
        details_separator.setFrameShape(QFrame.Shape.HLine)
        details_separator.setStyleSheet("background-color: #e2e8f0;")
        details_layout.addWidget(details_separator)

        # Items
        items = [
            ("Base Salary", self.invoice_data['amount']),
            ("Bonus", self.invoice_data['bonus'])
        ]

        for desc, amount in items:
            item_layout = QHBoxLayout()
            desc_label = QLabel(desc)
            amount_label = QLabel(amount)
            desc_label.setStyleSheet("color: #475569;")
            amount_label.setStyleSheet("color: #475569;")
            
            item_layout.addWidget(desc_label)
            item_layout.addStretch()
            item_layout.addWidget(amount_label)
            details_layout.addLayout(item_layout)

        # Total
        total_separator = QFrame()
        total_separator.setFrameShape(QFrame.Shape.HLine)
        total_separator.setStyleSheet("background-color: #e2e8f0;")
        details_layout.addWidget(total_separator)

        total_layout = QHBoxLayout()
        total_label = QLabel("Total")
        total_amount = QLabel(f"${float(self.invoice_data['amount'].replace('$','').replace(',','')) + float(self.invoice_data['bonus'].replace('$','').replace(',','')):.2f}")
        
        total_label.setStyleSheet("""
            font-weight: bold;
            color: #1e293b;
            font-size: 16px;
        """)
        total_amount.setStyleSheet("""
            font-weight: bold;
            color: #1e293b;
            font-size: 16px;
        """)
        
        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(total_amount)
        details_layout.addLayout(total_layout)

        card_layout.addWidget(details_frame)

        # Status
        status_layout = QHBoxLayout()
        status_label = QLabel("Status:")
        status_value = QLabel(self.invoice_data['status'])
        status_value.setStyleSheet(f"""
            color: white;
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: 500;
            background-color: {('#22c55e' if self.invoice_data['status'] == 'Paid' else '#f97316')};
        """)
        
        status_layout.addWidget(status_label)
        status_layout.addWidget(status_value)
        status_layout.addStretch()
        card_layout.addLayout(status_layout)

        # Add invoice card to scroll area
        scroll_layout.addWidget(invoice_card)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        # Buttons
        button_layout = QHBoxLayout()
        
        download_btn = QPushButton("Download PDF")
        download_btn.setStyleSheet("""
            QPushButton {
                background-color: #0ea5e9;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0284c7;
            }
        """)
        download_btn.clicked.connect(self.generate_pdf)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e2e8f0;
                color: #1e293b;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #cbd5e1;
            }
        """)
        
        if self.invoice_data['status'] == 'Pending':
            mark_paid_btn = QPushButton("Mark as Paid")
            mark_paid_btn.setStyleSheet("""
                QPushButton {
                    background-color: #22c55e;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #16a34a;
                }
            """)
            button_layout.addWidget(mark_paid_btn)

        button_layout.addWidget(download_btn)
        button_layout.addWidget(close_btn)
        
        close_btn.clicked.connect(self.close)
        main_layout.addLayout(button_layout)

    def generate_pdf(self, show_save_dialog=True):
        # Create a temporary file path for sending emails
        temp_path = os.path.join(os.path.dirname(__file__), f"temp_Invoice_{self.invoice_data['id']}.pdf")
        
        # Create PDF
        c = canvas.Canvas(temp_path, pagesize=letter)
        width, height = letter

        # Company Info
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, height - 50, "EMS Company")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 70, "123 Business Street")
        c.drawString(50, height - 85, "City, State 12345")
        c.drawString(50, height - 100, "Phone: (555) 123-4567")

        # Invoice Title and Details
        c.setFont("Helvetica-Bold", 32)
        c.setFillColor(colors.HexColor('#0ea5e9'))
        c.drawString(400, height - 50, "INVOICE")
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 12)
        c.drawString(400, height - 70, f"Invoice #: {self.invoice_data['id']}")
        c.drawString(400, height - 85, f"Date: {self.invoice_data['month']} {self.invoice_data['year']}")

        # Separator Line
        c.line(50, height - 120, width - 50, height - 120)

        # Bill To Section
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 150, "Bill To:")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 170, self.invoice_data['employee'])

        # Invoice Details
        y = height - 220
        
        # Headers
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Description")
        c.drawString(450, y, "Amount")
        
        # Separator
        y -= 10
        c.line(50, y, width - 50, y)
        
        # Items
        y -= 25
        c.setFont("Helvetica", 12)
        
        # Base Salary
        c.drawString(50, y, "Base Salary")
        c.drawString(450, y, self.invoice_data['amount'])
        
        # Bonus
        y -= 25
        c.drawString(50, y, "Bonus")
        c.drawString(450, y, self.invoice_data['bonus'])
        
        # Total Line
        y -= 20
        c.line(50, y, width - 50, y)
        
        # Total Amount
        y -= 25
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Total")
        total = float(self.invoice_data['amount'].replace('$','').replace(',','')) + \
               float(self.invoice_data['bonus'].replace('$','').replace(',',''))
        c.drawString(450, y, f"${total:,.2f}")

        # Status
        y -= 50
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Status:")
        c.setFont("Helvetica", 12)
        status_color = '#22c55e' if self.invoice_data['status'] == 'Paid' else '#f97316'
        c.setFillColor(colors.HexColor(status_color))
        c.drawString(100, y, self.invoice_data['status'])

        c.save()
        
        # If this was called from the UI button and show_save_dialog is True
        if self.parent() and show_save_dialog:
            file_name = f"Invoice_{self.invoice_data['id']}.pdf"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Invoice",
                file_name,
                "PDF Files (*.pdf)"
            )
            
            if file_path:
                # Copy the temp file to the selected location
                import shutil
                shutil.copy2(temp_path, file_path)
                
                # Clean up temp file
                try:
                    os.remove(temp_path)
                except:
                    pass
                    
                return file_path
        
        return temp_path