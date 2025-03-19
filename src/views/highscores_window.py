from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QTableWidget,
                           QTableWidgetItem, QComboBox, QHBoxLayout)
from PyQt6.QtCore import Qt

class HighscoresWindow(QDialog):
    def __init__(self, highscore_model, parent=None):
        super().__init__(parent)
        self.highscore_model = highscore_model
        
        self.setWindowTitle("Tipptest - Highscores")
        self.setFixedSize(600, 400)
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
        
        # Tabelle für Highscores
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Platz", "Name", "Punkte", "WPM", "Dauer", "Datum"])
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
        
        for row, highscore in enumerate(highscores):
            # Platz
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            # Name
            self.table.setItem(row, 1, QTableWidgetItem(highscore.name))
            # Punkte
            self.table.setItem(row, 2, QTableWidgetItem(str(highscore.score)))
            # WPM
            self.table.setItem(row, 3, QTableWidgetItem(str(highscore.words_per_minute)))
            # Dauer
            self.table.setItem(row, 4, QTableWidgetItem(f"{highscore.duration} Min."))
            # Datum
            self.table.setItem(row, 5, QTableWidgetItem(highscore.date))