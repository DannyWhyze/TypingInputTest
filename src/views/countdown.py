from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt, pyqtSignal

class CountdownWidget(QWidget):
    # Signal für Timer-Ende
    timerFinished = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self.model = model
        
        # Layout erstellen
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(3)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Überschrift
        self.title_label = QLabel("Countdown")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.title_label)
        
        # Zeit-Anzeige
        self.time_label = QLabel("00:00")
        self.time_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            padding: 5px;
        """)
        self.layout.addWidget(self.time_label)
        
        # Timer für das regelmäßige Update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.setInterval(1000)  # Aktualisiere alle 1000ms (1 Sekunde)
        
        # Mindestgröße setzen
        self.setMinimumWidth(120)
        self.setMinimumHeight(80)
        
    def update_display(self):
        """Aktualisiert die Timer-Anzeige"""
        if self.model.update_timer():
            # Timer läuft noch, aktualisiere Anzeige
            self.time_label.setText(self.model.get_time_remaining_str())
        else:
            # Timer ist abgelaufen
            self.time_label.setText("00:00")
            self.timer.stop()
            # Signal auslösen, dass der Timer abgelaufen ist
            self.timerFinished.emit()
    
    def start_timer(self):
        """Startet die Timer-Anzeige"""
        if self.model.timer_active:
            self.timer.start()
            self.update_display()  # Sofort aktualisieren
    
    def stop_timer(self):
        """Stoppt die Timer-Anzeige"""
        self.timer.stop()

    def show_initial_time(self):
        """
        Zeigt die initial eingestellte Zeit an, ohne den Timer zu starten.
        """
        # Zeit im Label anzeigen
        self.time_label.setText(self.model.get_time_remaining_str())