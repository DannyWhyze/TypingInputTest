from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

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

        # Widget insgesamt größer machen
        self.setMinimumWidth(120)
        self.setMinimumHeight(60)

    def update_info(self):
        """Aktualisiert die Anzeige der Anschlagszahl."""
        self.label_text.setText(f"Anschläge: {self.model.keystroke_count}")
