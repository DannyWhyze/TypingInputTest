from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from src.models.statisticsModel import StatisticsModel
from src.views.statistics_widget import StatisticsWidget

class ResultsWindow(QDialog):
    def __init__(self, model, parent=None, stats_model=None):
        super().__init__(parent)
        self.model = model
        
        # StatisticsModel verwenden oder neu erstellen
        self.statistics_model = stats_model if stats_model else StatisticsModel(model)
        
        self.setWindowTitle("Tipptest - Ergebnisse")
        self.setFixedSize(550, 500)  # Vergrößert für die Statistik
        self.setModal(True)
        
        # Hauptlayout
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(30, 30, 30, 30)
        
        # Überschrift
        title_label = QLabel("Tippen beendet - Deine Ergebnisse")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)
        
        # Ergebnisse anzeigen
        self.create_results_section()
        
        # Tippgenauigkeit-Statistik
        self.create_accuracy_section()
        
        # Buttons am unteren Rand
        self.create_button_row()
        
        # Platz am Ende
        self.layout.addStretch(1)
        
    def create_results_section(self):
        """Erstellt die Anzeige der Ergebnisse"""
        # Statistik berechnen
        keystroke_count = self.model.keystroke_count
        time_in_minutes = self.model.timer_duration / 60
        keystrokes_per_minute = round(keystroke_count / time_in_minutes, 1)
        
        # Ergebniscontainer
        results_layout = QVBoxLayout()
        
        # Ergebniszeilen
        results_data = [
            ("Gesamte Tastenanschläge:", f"{keystroke_count}"),
            ("Zeit:", f"{int(time_in_minutes)} Minute(n)"),
            ("Anschläge pro Minute:", f"{keystrokes_per_minute}"),
            # Die Zeile für Anschläge pro Sekunde wurde entfernt
        ]
        
        # Jede Ergebniszeile erstellen
        for label_text, value_text in results_data:
            row = QHBoxLayout()
            
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 16px;")
            row.addWidget(label)
            
            value = QLabel(value_text)
            value.setStyleSheet("font-size: 16px; font-weight: bold; color: #2a5885;")
            row.addWidget(value)
            
            # Rechts ausrichten
            row.setStretchFactor(label, 1)
            row.setStretchFactor(value, 0)
            
            results_layout.addLayout(row)
        
        self.layout.addLayout(results_layout)
    
    def create_accuracy_section(self):
        """Erstellt den Tippgenauigkeit-Bereich"""
        # Trennlinie
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setLineWidth(1)
        self.layout.addWidget(separator)
        
        # Überschrift
        accuracy_title = QLabel("Tippgenauigkeit")
        accuracy_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        accuracy_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(accuracy_title)
        
        # Statistik berechnen
        typed_text = self.get_typed_text()
        statistics = self.statistics_model.calculate_typing_statistics(typed_text)
        
        # StatisticsWidget erstellen und hinzufügen - jetzt mit Referenz zum stats_model
        stats_widget = StatisticsWidget(statistics, self.statistics_model)
        self.layout.addWidget(stats_widget)
        
    def get_typed_text(self):
        """
        Holt den getippten Text vom Hauptfenster
        """
        parent = self.parent()
        if parent and hasattr(parent, 'input_field'):
            return parent.input_field.get_text()
        return ""  # Fallback, wenn kein Text verfügbar
    
    def create_button_row(self):
        """Erstellt die Reihe mit Buttons am Ende des Dialogs"""
        button_row = QHBoxLayout()
        
        # Neuer Test Button
        new_test_button = QPushButton("Neuer Test")
        new_test_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        new_test_button.clicked.connect(self.restart_test)
        
        # Beenden Button
        exit_button = QPushButton("Beenden")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        exit_button.clicked.connect(self.close_application)
        
        button_row.addWidget(new_test_button)
        button_row.addWidget(exit_button)
        
        self.layout.addLayout(button_row)
        
    def restart_test(self):
        """Startet einen neuen Test"""
        # Dialog schließen
        self.accept()
        
        # Hauptfenster zurücksetzen (wird im aufrufenden Code implementiert)
        parent = self.parent()
        if parent and hasattr(parent, 'reset_for_new_test'):
            parent.reset_for_new_test()
    
    def close_application(self):
        """Beendet die Anwendung"""
        self.reject()  # Dialog ablehnen (schließen)
        # Hauptfenster schließen
        parent = self.parent()
        if parent:
            parent.close()