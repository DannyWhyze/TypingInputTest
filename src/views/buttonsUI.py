from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
from src.utils.labels import Labels
from src.views.tip_info import TipInfo
from src.models.highscore_model import HighscoreModel
from src.views.highscores_window import HighscoresWindow

class ButtonsUI(QWidget):
    def __init__(self, model):
        """
        Widget mit drei Buttons, Label für "Minute(n)" und einem Tippinfo-Widget rechts daneben.
        """
        super().__init__()
        self.model = model
        
        # Highscore-Model initialisieren
        self.highscore_model = HighscoreModel()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 5, 10, 5)

        # Linker Bereich: Timer-Buttons und Label
        left_widget = QWidget()
        left_layout = QHBoxLayout(left_widget)
        left_layout.setSpacing(0)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        button_style = """
        QPushButton {
            margin: 0;
            padding: 0;
            border: 1px solid #888;
        }
        """

        # Button "1" mit Click-Handler
        self.button1 = QPushButton("1")
        self.button1.setFixedSize(50, 30)
        self.button1.setStyleSheet(button_style)
        self.button1.clicked.connect(lambda: self.set_timer_minutes(1))
        left_layout.addWidget(self.button1)

        # Button "3" mit Click-Handler
        self.button3 = QPushButton("3")
        self.button3.setFixedSize(50, 30)
        self.button3.setStyleSheet(button_style)
        self.button3.clicked.connect(lambda: self.set_timer_minutes(3))
        left_layout.addWidget(self.button3)

        # Button "5" mit Click-Handler
        self.button5 = QPushButton("5")
        self.button5.setFixedSize(50, 30)
        self.button5.setStyleSheet(button_style)
        self.button5.clicked.connect(lambda: self.set_timer_minutes(5))
        left_layout.addWidget(self.button5)

        left_layout.addSpacing(5)

        # Label "Minute(n)"
        self.minute_label = QLabel(Labels.MINUTE_LABEL)
        self.minute_label.setStyleSheet("font-size: 16px;")
        left_layout.addWidget(self.minute_label)
        
        # Linken Bereich zum Hauptlayout hinzufügen
        self.layout.addWidget(left_widget)
        
        # Flexible Lücke einfügen, aber nur links vom Tip Info
        self.layout.addStretch(1)
        
        # Mittlerer Bereich: Alle Elemente in der Mitte zusammengefasst
        middle_widget = QWidget()
        middle_layout = QHBoxLayout(middle_widget)
        middle_layout.setSpacing(15)  # Mehr Abstand zwischen den Elementen
        middle_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tippinfo-Widget
        self.tip_info = TipInfo(self.model)
        middle_layout.addWidget(self.tip_info)
        
        # Highscores Button direkt neben dem Tip Info
        self.highscores_button = QPushButton("Highscores")
        self.highscores_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 8px 15px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.highscores_button.setFixedSize(120, 35)
        self.highscores_button.clicked.connect(self.show_highscores)
        middle_layout.addWidget(self.highscores_button)
        
        # Ergebnis-Button direkt neben dem Highscore-Button
        self.results_button = QPushButton("Ergebnis")
        self.results_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 8px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.results_button.setFixedSize(120, 35)
        middle_layout.addWidget(self.results_button)
        self.results_button.hide()  # Initial verstecken
        
        # Mittleren Bereich zum Hauptlayout hinzufügen
        self.layout.addWidget(middle_widget)
        
        # Flexible Lücke auf der rechten Seite, um alle Elemente nach links zu rücken
        self.layout.addStretch(1)
        
    def set_timer_minutes(self, minutes):
        """
        Setzt den Timer auf die angegebene Minutenzahl, zeigt ihn an, startet ihn aber noch nicht.
        """
        if self.model.set_timer(minutes):
            # Timer nicht starten, aber anzeigen
            print(f"Timer auf {minutes} Minute(n) gesetzt und wartet auf Tippbeginn.")
            
            # Countdown-Widget aktualisieren, ohne den Timer zu starten
            window = self.window()
            if hasattr(window, 'countdown'):
                window.countdown.show_initial_time()
    
    def show_results_button(self):
        """Zeigt den Ergebnis-Button an."""
        self.results_button.show()
        self.results_button.clicked.connect(self.open_results_window)

    def open_results_window(self):
        """Öffnet das Ergebnisfenster"""
        from src.views.results_window import ResultsWindow
        
        # Dialog erstellen und öffnen
        window = self.window()
        if hasattr(window, 'stats_model'):
            results_dialog = ResultsWindow(self.model, window, stats_model=window.stats_model)
        else:
            results_dialog = ResultsWindow(self.model, window)
        results_dialog.exec()  # Modal öffnen (blockiert bis Dialog geschlossen wird)
        
    def show_highscores(self):
        """Zeigt das Highscore-Fenster an"""
        highscores_dialog = HighscoresWindow(self.highscore_model, self.window())
        highscores_dialog.exec()