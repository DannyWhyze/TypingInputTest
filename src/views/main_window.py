from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from src.views.buttonsUI import ButtonsUI
from src.models.main_model import MainModel
from src.views.input_field import InputField
from src.views.countdown import CountdownWidget
from src.views.textinfos import TextInfo
from src.views.target_text_widget import TargetTextWidget
from src.views.menu_bar import ApplicationMenuBar  # Importiere die neue Menüleistenklasse

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tipptraining")
        self.model = MainModel()
        # StatisticsModel zentral erstellen
        from src.models.statisticsModel import StatisticsModel
        self.stats_model = StatisticsModel(self.model)
        
        # Menüleiste einrichten (vor initUI)
        self.menu_bar = ApplicationMenuBar(self)
        self.setMenuBar(self.menu_bar)
        
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
        # Signal-Verbindung für Timer-Ende hinzufügen
        self.countdown.timerFinished.connect(self.timer_finished)  # Neue Verbindung
        self.countdown.timerFinished.connect(self.buttons.show_results_button)
        input_area.addWidget(self.countdown)
        
        # Eingabefeld rechts - jetzt mit dem zentralen StatisticsModel
        self.input_field = InputField(self.model, self.target_text, stats_model=self.stats_model)
        input_area.addWidget(self.input_field)
        
        # Horizontales Layout zum Hauptlayout hinzufügen
        main_layout.addLayout(input_area)
        
        # Extra Platz nach unten schieben
        main_layout.addStretch(1)
        
    def start_countdown(self):
        """Startet den Countdown nach Button-Klick"""
        self.countdown.start_timer()

    def reset_for_new_test(self):
        """Setzt die Anwendung für einen neuen Test zurück"""
        # Model zurücksetzen
        self.model.reset_timer()
        self.model.keystroke_count = 0
        
        # UI-Elemente zurücksetzen
        self.input_field.clear_text()
        self.input_field.countdown_started = False
        self.countdown.time_label.setText("00:00")
        self.target_text.refresh_text()
        self.buttons.results_button.hide()
        
        # Eingabefeld wieder aktivieren (dies fehlte)
        self.input_field.text_edit.setReadOnly(False)
        # Styling für aktives Eingabefeld wiederherstellen
        self.input_field.text_edit.setStyleSheet("""
            QTextEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)

    def timer_finished(self):
        """Wird aufgerufen, wenn der Timer abläuft"""
        # Eingabefeld deaktivieren
        self.input_field.text_edit.setReadOnly(True)
        # Optional: Visuellen Hinweis geben
        self.input_field.text_edit.setStyleSheet("""
            QTextEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f0f0f0;  /* Hellgrauer Hintergrund zur Indikation */
            }
        """)
        # Fokus auf das Fenster setzen (Cursor aus dem Eingabefeld nehmen)
        self.setFocus()