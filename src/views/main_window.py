from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTextEdit
from PyQt6.QtCore import Qt
from .buttonsUI import ButtonsUI  # Relativer Import statt absolutem Import

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Container erstellen
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Hauptlayout mit absolut keinen Abständen
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Buttons hinzufügen (fest oben)
        self.buttons = ButtonsUI()
        main_layout.addWidget(self.buttons)
        
        # Textfeld DIREKT darunter (kein eigenes Widget, um Verschachtelung zu vermeiden)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Type your multiline text here...")
        self.text_edit.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                padding: 5px;
                margin: 0px;
                border-top: 0px;
            }
        """)
        main_layout.addWidget(self.text_edit)
        
        # Extra Platz nach unten schieben
        main_layout.addStretch(1)