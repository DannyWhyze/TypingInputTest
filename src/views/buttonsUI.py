from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
from src.utils.labels import Labels
from src.views.tip_info import TipInfo

class ButtonsUI(QWidget):
    def __init__(self, model):
        """
        Widget mit drei Buttons, Label für "Minute(n)" und einem Tippinfo-Widget rechts daneben.
        """
        super().__init__()
        self.model = model

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10, 0, 0, 0)

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
        self.layout.addWidget(self.button1)

        # Button "3" mit Click-Handler
        self.button3 = QPushButton("3")
        self.button3.setFixedSize(50, 30)
        self.button3.setStyleSheet(button_style)
        self.button3.clicked.connect(lambda: self.set_timer_minutes(3))
        self.layout.addWidget(self.button3)

        # Button "5" mit Click-Handler
        self.button5 = QPushButton("5")
        self.button5.setFixedSize(50, 30)
        self.button5.setStyleSheet(button_style)
        self.button5.clicked.connect(lambda: self.set_timer_minutes(5))
        self.layout.addWidget(self.button5)

        self.layout.addSpacing(5)

        # Label "Minute(n)"
        self.minute_label = QLabel(Labels.MINUTE_LABEL)
        self.minute_label.setStyleSheet("font-size: 16px;")
        self.layout.addWidget(self.minute_label)

        # Neues Tippinfo-Widget rechts daneben
        self.layout.addSpacing(10)
        self.tip_info = TipInfo(self.model)
        self.layout.addWidget(self.tip_info)
        
        # Ergebnis-Button (initial unsichtbar)
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
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.results_button.setFixedSize(120, 35)
        self.layout.addWidget(self.results_button)
        self.results_button.hide()  # Initial verstecken

        self.setFixedWidth(650)  # Erhöht wegen des zusätzlichen Buttons
        
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