from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from src.views.buttonsUI import ButtonsUI
from src.models.main_model import MainModel
from src.views.input_field import InputField
from src.views.countdown import CountdownWidget
from src.views.textinfos import TextInfo
from src.views.target_text_widget import TargetTextWidget

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
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Buttons hinzufügen (fest oben)
        self.buttons = ButtonsUI(self.model)
        main_layout.addWidget(self.buttons)
        
        # TextInfo-Widget hinzufügen (zwischen Buttons und Input-Area)
        self.text_info = TextInfo()
        main_layout.addWidget(self.text_info)
        
        # Zieltext-Widget (zu tippender Text)
        self.target_text = TargetTextWidget(self.model)
        main_layout.addWidget(self.target_text)
        
        # Horizontales Layout für Timer und InputField
        input_area = QHBoxLayout()
        
        # Timer-Widget links
        self.countdown = CountdownWidget(self.model)
        input_area.addWidget(self.countdown)
        
        # Eingabefeld rechts - jetzt mit Verweis auf das TargetTextWidget
        self.input_field = InputField(self.model, self.target_text)
        input_area.addWidget(self.input_field)
        
        # Horizontales Layout zum Hauptlayout hinzufügen
        main_layout.addLayout(input_area)
        
        # Extra Platz nach unten schieben
        main_layout.addStretch(1)
        
    def start_countdown(self):
        """Startet den Countdown nach Button-Klick"""
        self.countdown.start_timer()