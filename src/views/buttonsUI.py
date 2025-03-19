from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
from src.utils.labels import Labels  # Absoluter Import

class ButtonsUI(QWidget):
    def __init__(self):
        """
        Erstellt ein Widget mit drei Buttons, die ohne Abstand nebeneinander liegen,
        und einem Label rechts daneben.
        """
        super().__init__()
        # Kein automatisches Dehnen im Container
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # Layout ohne Parent erstellen (wichtig!)
        self.layout = QHBoxLayout(self)
        
        # Komplett alle Abstände entfernen
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10, 0, 0, 0)  # Kleiner linker Rand
        
        # Button-Style ohne interne Abstände
        button_style = """
        QPushButton {
            margin: 0;
            padding: 0;
            border: 1px solid #888;
        }
        """
        
        # Button "1" 
        self.button1 = QPushButton("1")
        self.button1.setFixedSize(50, 30)
        self.button1.setStyleSheet(button_style)
        self.layout.addWidget(self.button1)
        
        # Button "3"
        self.button3 = QPushButton("3")
        self.button3.setFixedSize(50, 30)
        self.button3.setStyleSheet(button_style)
        self.layout.addWidget(self.button3)
        
        # Button "5"
        self.button5 = QPushButton("5")
        self.button5.setFixedSize(50, 30)
        self.button5.setStyleSheet(button_style)
        self.layout.addWidget(self.button5)
        
        # Minimaler Abstand vor dem Label
        self.layout.addSpacing(5)
        
        # Label "Minute(n)" hinzufügen
        self.minute_label = QLabel(Labels.MINUTE_LABEL)
        self.minute_label.setStyleSheet("font-size: 16px;")  # Größere Schrift
        self.layout.addWidget(self.minute_label)
        
        # Wichtig: Verhindere, dass das Layout den Platz ausfüllt
        # self.layout.addStretch(1)  <- Diese Zeile entfernen!
        
        # Gesamtbreite auf exakt die Button-Breite festlegen
        self.setFixedWidth(320)  # 3 buttons × 40px width