from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QTableWidget,
                           QTableWidgetItem, QComboBox, QHBoxLayout, QHeaderView)
from PyQt6.QtCore import Qt

class HighscoresWindow(QDialog):
    def __init__(self, highscore_model, parent=None):
        super().__init__(parent)
        self.highscore_model = highscore_model
        
        self.setWindowTitle("Tipptest - Highscores")
        self.setFixedSize(900, 400)
        self.setModal(True)
        
        # Hauptlayout
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Überschrift
        title_label = QLabel("Highscores")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)
        
        # Filter für Testdauer
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter nach Testdauer:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Alle", None)
        self.filter_combo.addItem("1 Minute", 1)
        self.filter_combo.addItem("3 Minuten", 3)
        self.filter_combo.addItem("5 Minuten", 5)
        self.filter_combo.currentIndexChanged.connect(self.update_table)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch(1)
        self.layout.addLayout(filter_layout)
        
        # Tabelle für Highscores mit überarbeiteten Spalten
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        
        # Spaltenüberschriften mit mehrzeiligen Texten
        self.table.setHorizontalHeaderLabels([
            "Platz", 
            "Name", 
            "Punkte", 
            "Zeichen\npro Minute", 
            "Fehler\npro Minute", 
            "Maximale\nZeichen/Sek", 
            "Dauer", 
            "Datum"
        ])
        
        # Höhe der Header-Zeile vergrößern für mehrzeilige Beschriftungen
        self.table.horizontalHeader().setMinimumHeight(45)
        
        # Spaltenbreiten anpassen und Tabelle konfigurieren
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)
        
        # Schließen-Button
        close_button = QPushButton("Schließen")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.layout.addWidget(close_button)
        
        # Tabelle initial befüllen
        self.update_table()
        
    def update_table(self):
        """Aktualisiert die Highscore-Tabelle basierend auf dem ausgewählten Filter"""
        duration_filter = self.filter_combo.currentData()
        highscores = self.highscore_model.get_highscores(duration=duration_filter)
        
        self.table.setRowCount(len(highscores))
        
        # Spaltenbreiten setzen
        self.table.setColumnWidth(0, 50)   # Platz
        self.table.setColumnWidth(1, 150)  # Name
        self.table.setColumnWidth(2, 80)   # Punkte
        self.table.setColumnWidth(3, 100)  # Zeichen pro Minute
        self.table.setColumnWidth(4, 100)  # Fehler pro Minute
        self.table.setColumnWidth(5, 100)  # Max. Zeichen pro Sekunde
        self.table.setColumnWidth(6, 80)   # Dauer
        self.table.setColumnWidth(7, 150)  # Datum
        
        for row, highscore in enumerate(highscores):
            # Platz
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            # Name
            self.table.setItem(row, 1, QTableWidgetItem(highscore.name))
            # Punkte
            self.table.setItem(row, 2, QTableWidgetItem(str(highscore.score)))
            # Zeichen pro Minute
            self.table.setItem(row, 3, QTableWidgetItem(str(highscore.chars_per_minute)))
            # Fehler pro Minute
            self.table.setItem(row, 4, QTableWidgetItem(str(highscore.errors_per_minute)))
            # Max. Zeichen pro Sekunde
            self.table.setItem(row, 5, QTableWidgetItem(str(highscore.max_chars_per_second)))
            # Dauer
            self.table.setItem(row, 6, QTableWidgetItem(f"{highscore.duration} Min."))
            # Datum
            self.table.setItem(row, 7, QTableWidgetItem(highscore.date))