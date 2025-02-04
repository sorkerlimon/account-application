import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from login import LoginWindow

def main():
    print("Starting application...")
    app = QApplication(sys.argv)
    
    # Set the style to Fusion
    app.setStyle("Fusion")
    print("Style set to Fusion")
    
    # Create dark palette for modern look
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#f0f2f5"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#1a202c"))
    app.setPalette(palette)
    
    # Create and show login window
    login_window = LoginWindow()
    print("Login window created and shown")
    login_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
