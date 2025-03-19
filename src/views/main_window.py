from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from src.views.buttonsUI import ButtonsUI
from src.models.main_model import MainModel
from src.views.input_field import InputField
from src.views.countdown import CountdownWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)
        
        # Model erzeugen
        self.model = MainModel()
        self.initUI()

    def initUI(self):
        # Container erstellen
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Hauptlayout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Buttons hinzufügen (fest oben)
        self.buttons = ButtonsUI(self.model)
        main_layout.addWidget(self.buttons)
        
        # Horizontales Layout für Timer und InputField
        input_area = QHBoxLayout()
        
        # Timer-Widget links
        self.countdown = CountdownWidget(self.model)
        input_area.addWidget(self.countdown)
        
        # Eingabefeld rechts
        self.input_field = InputField(self.model, "Type your multiline text here...")
        input_area.addWidget(self.input_field)
        
        # Horizontales Layout zum Hauptlayout hinzufügen
        main_layout.addLayout(input_area)
        
        # Extra Platz nach unten schieben
        main_layout.addStretch(1)
        
        # Entferne diese Verbindungen:
        # self.buttons.button1.clicked.connect(self.start_countdown)
        # self.buttons.button3.clicked.connect(self.start_countdown)
        # self.buttons.button5.clicked.connect(self.start_countdown)
    
    def start_countdown(self):
        """Startet den Countdown nach Button-Klick"""
        self.countdown.start_timer()