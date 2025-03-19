from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer

class TipInfo(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model

        # Vertikales Layout für "Tippinfo" und "Anschläge"
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(3)

        # Überschrift "Tippinfo" erstellen und zentrieren
        self.title_label = QLabel("Tippinfo")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Zeile mit Anschlägen – zentriert
        self.label_text = QLabel(f"Anschläge: {self.model.keystroke_count}")
        self.label_text.setStyleSheet("font-size: 14px;")
        self.label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_text)

        # Zeile mit Anschlägen pro Sekunde – zentriert
        self.label_speed = QLabel(f"Anschläge pro Sekunde: 0.0/s")
        self.label_speed.setStyleSheet("font-size: 14px;")
        self.label_speed.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_speed)

        # Widget-Größe
        self.setMinimumWidth(250)
        self.setMinimumHeight(85)

        # Timer zur Aktualisierung
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_info)
        self.update_timer.start(1000)

    def update_info(self):
        self.label_text.setText(f"Anschläge: {self.model.keystroke_count}")
        keystroke_speed = self.model.get_keystrokes_per_second()
        self.label_speed.setText(f"Anschläge pro Sekunde: {keystroke_speed}/s")
