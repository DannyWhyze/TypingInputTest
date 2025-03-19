from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
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
        # Flag für manuellen Reset
        self.manual_reset = False
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
        main_layout.addWidget(self.text_info, alignment=Qt.AlignmentFlag.AlignCenter)
        
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
        
        # Neustarten-Button unter dem Eingabefeld (horizontal zentriert)
        restart_container = QHBoxLayout()
        restart_container.addStretch(1)
        
        self.restart_button = QPushButton("Neu starten")
        self.restart_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 8px 15px;
                background-color: #ff9800;
                color: white;
                border: none;
                border-radius: 5px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.restart_button.setEnabled(False)  # Initial deaktiviert
        self.restart_button.clicked.connect(self.reset_for_new_test)
        restart_container.addWidget(self.restart_button)
        restart_container.addStretch(1)
        
        main_layout.addLayout(restart_container)
        
        # Extra Platz nach unten schieben
        main_layout.addStretch(1)
        
    def start_countdown(self):
        """Startet den Countdown nach Button-Klick"""
        self.countdown.start_timer()

    def reset_for_new_test(self):
        """Setzt die Anwendung für einen neuen Test zurück"""
        # Timer stoppen, sodass kein timerFinished-Signal mehr emittiert wird
        self.countdown.stop_timer()
        
        # Model zurücksetzen
        self.model.timer_duration = 0
        self.model.time_remaining = 0
        self.model.keystroke_count = 0
        
        # UI-Elemente zurücksetzen
        self.input_field.clear_text()
        self.input_field.countdown_started = False
        self.countdown.time_label.setText("00:00")
        self.target_text.refresh_text()
        
        # Ergebnis-Button deaktivieren und eventuelle Click-Signale trennen
        if hasattr(self, 'buttons') and hasattr(self.buttons, 'results_button'):
            self.buttons.results_button.setEnabled(False)
            # Falls Click-Signale verbunden sind, trenne sie:
            try:
                self.buttons.results_button.clicked.disconnect()
            except Exception:
                pass
        
        # Eingabefeld wieder aktivieren
        self.input_field.text_edit.setReadOnly(False)
        self.input_field.text_edit.setStyleSheet("""
            QTextEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        
        # Neustart-Button deaktivieren bis zum nächsten Tippbeginn
        self.restart_button.setEnabled(False)
        
        # Hinweistext aktualisieren
        self.text_info.info_label.setText("Bitte wähle eine Zeitdauer (1, 3 oder 5 Minuten) und tippe dann den Text ab.")

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