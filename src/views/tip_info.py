from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer

class TipInfo(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model

        # Vertikales Layout für "Tippinfo" und "Anschläge"
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # Mehr Abstand im Layout
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(3)  # Mehr Abstand zwischen den Labels

        # Überschrift mit größerer Schrift
        self.title_label = QLabel("Tippinfo:")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")  # Größere Schrift
        self.layout.addWidget(self.title_label)

        # Zeile mit Anschlägen - auch größere Schrift
        self.label_text = QLabel(f"Anschläge: {self.model.keystroke_count}")
        self.label_text.setStyleSheet("font-size: 14px;")  # Größere Schrift
        self.layout.addWidget(self.label_text)

        # Zeile mit Anschlägen pro Sekunde
        self.label_speed = QLabel(f"Anschläge pro Sekunde: 0.0/s")
        self.label_speed.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.label_speed)

        # Widget insgesamt größer machen
        self.setMinimumWidth(250)  # Erhöht von 180 auf 220 für breitere Anzeige
        self.setMinimumHeight(85)  # Höhe bleibt gleich

        # Timer für regelmäßige Updates der Anzeige
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_info)
        self.update_timer.start(1000)  # Update alle Sekunde

    def update_info(self):
        """Aktualisiert die Anzeige der Anschlagszahl und Anschläge pro Sekunde."""
        self.label_text.setText(f"Anschläge: {self.model.keystroke_count}")
        
        # Anschläge pro Sekunde aktualisieren
        keystroke_speed = self.model.get_keystrokes_per_second()
        self.label_speed.setText(f"Anschläge pro Sekunde: {keystroke_speed}/s")
