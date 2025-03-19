from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class TextInfo(QWidget):
    def __init__(self, text=None):
        super().__init__()
        
        # Standard-Text, falls keiner übergeben wird
        if text is None:
            text = "Bitte tippe den folgenden Text ab. Der Countdown beginnt zu laufen, sobald der erste Tastenanschlag erfolgt."
        
        # Layout erstellen
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(0)
        
        # Label für den Text erstellen
        self.info_label = QLabel(text)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setWordWrap(True)
        
        # Styling für deutlichere Abhebung
        self.setStyleSheet("""
            QWidget {
                background-color: #e0e8f0;  /* Bläulicher Grauton */
                border-radius: 10px;
                padding: 8px;
                border: 1px solid #c0c0c0;  /* Feiner Rahmen für zusätzliche Abgrenzung */
            }
            QLabel {
                font-size: 14px;
                color: #333;
                background-color: transparent;
            }
        """)
        
        # Label zum Layout hinzufügen
        self.layout.addWidget(self.info_label)