from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, 
                           QLineEdit, QMessageBox, QWidget)  # QWidget hinzugefügt
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
        
        # Flag, um zu verfolgen, ob ein Highscore bereits gespeichert wurde
        self.highscore_saved = False
        
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
        
        # Highscore-Eingabebereich (anfangs unsichtbar)
        self.highscore_input_widget = QWidget()
        self.highscore_input_layout = QHBoxLayout(self.highscore_input_widget)
        
        self.highscore_name_label = QLabel("Name:")
        self.highscore_name_input = QLineEdit()
        self.highscore_name_input.setMaxLength(20)
        
        self.highscore_save_button = QPushButton("Speichern")
        self.highscore_save_button.clicked.connect(self.save_highscore)
        self.highscore_save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.highscore_cancel_button = QPushButton("Abbrechen")
        self.highscore_cancel_button.clicked.connect(self.hide_highscore_input)
        self.highscore_cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        
        self.highscore_input_layout.addWidget(self.highscore_name_label)
        self.highscore_input_layout.addWidget(self.highscore_name_input, 1)
        self.highscore_input_layout.addWidget(self.highscore_save_button)
        self.highscore_input_layout.addWidget(self.highscore_cancel_button)
        
        # Anfangs verstecken
        self.highscore_input_widget.hide()
        
        # Zum Layout hinzufügen (vor Button-Zeile)
        self.layout.addWidget(self.highscore_input_widget)
        
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
        
        # Punktzahl und Boni berechnen
        typed_text = self.get_typed_text()
        
        # Grundpunkte
        base_points = len([c for c in self.statistics_model.main_model.check_typing(typed_text) if c == 1])
        
        # Boni
        sequence_bonus = self.statistics_model.calculate_word_sequence_bonus(typed_text)
        speed_bonus = self.statistics_model.calculate_speed_bonus()
        consistency_bonus = self.statistics_model.calculate_consistency_bonus()
        
        # Gesamtpunktzahl
        score = self.statistics_model.calculate_score(typed_text)

        # Ergebniscontainer
        results_layout = QVBoxLayout()
        
        # Ergebniszeilen
        results_data = [
            ("Gesamte Tastenanschläge:", f"{keystroke_count}"),
            ("Zeit:", f"{int(time_in_minutes)} Minute(n)"),
            ("Anschläge pro Minute:", f"{keystrokes_per_minute}"),
            ("Grundpunkte:", f"{base_points}"),
            ("Sequenz-Bonus:", f"{sequence_bonus}"),
            ("Geschwindigkeits-Bonus:", f"{speed_bonus}"),
            ("Konstanz-Bonus:", f"{consistency_bonus}"),
            ("Erzielte Punkte:", f"{score}"),
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
        
        # Highscore-Button
        highscore_button = QPushButton("Highscore speichern")
        highscore_button.setFixedWidth(150)  # Breite erhöhen von 120 auf 150
        highscore_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        highscore_button.clicked.connect(self.show_highscore_input)
        
        # Highscores-anzeigen-Button
        show_highscores_button = QPushButton("Highscores anzeigen")
        show_highscores_button.setFixedWidth(150)  # Breite erhöhen von 120 auf 150
        show_highscores_button.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        show_highscores_button.clicked.connect(self.show_highscores)
        
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
        
        # Buttons zum Layout hinzufügen
        button_row.addWidget(highscore_button)
        button_row.addWidget(show_highscores_button)
        button_row.addWidget(new_test_button)
        button_row.addWidget(exit_button)
        
        self.layout.addLayout(button_row)
    
    def show_highscore_input(self):
        """Zeigt das Eingabefeld für den Highscore-Namen an"""
        self.highscore_input_widget.show()
        self.highscore_name_input.setFocus()
    
    def hide_highscore_input(self):
        """Versteckt das Eingabefeld für den Highscore-Namen"""
        self.highscore_input_widget.hide()
    
    def save_highscore(self):
        """Speichert den aktuellen Highscore"""
        # Prüfen, ob bereits gespeichert wurde
        if self.highscore_saved:
            QMessageBox.information(self, "Information", "Du hast deinen Highscore bereits gespeichert!")
            self.hide_highscore_input()
            return
            
        name = self.highscore_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Fehler", "Bitte gib deinen Namen ein.")
            return
        
        # Daten für den Highscore sammeln
        typed_text = self.get_typed_text()
        score = self.statistics_model.calculate_score(typed_text)
        duration = self.model.timer_duration // 60  # Von Sekunden zu Minuten
        keystrokes_per_minute = round(self.model.keystroke_count / (self.model.timer_duration / 60), 1)
        
        # Den Highscore speichern
        parent = self.parent()
        if parent and hasattr(parent, 'buttons') and hasattr(parent.buttons, 'highscore_model'):
            parent.buttons.highscore_model.add_highscore(name, score, duration, keystrokes_per_minute)
            QMessageBox.information(self, "Erfolg", f"Dein Highscore wurde gespeichert, {name}!")
            self.hide_highscore_input()
            # Flag setzen, dass gespeichert wurde
            self.highscore_saved = True
            
            # Optional: Button deaktivieren, um visuelles Feedback zu geben
            for button in self.findChildren(QPushButton):
                if button.text() == "Highscore speichern":
                    button.setEnabled(False)
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #9e9e9e;
                            color: white;
                            font-size: 14px;
                            padding: 10px;
                            border-radius: 5px;
                        }
                    """)
                    break
        else:
            QMessageBox.warning(self, "Fehler", "Highscore konnte nicht gespeichert werden.")
    
    def show_highscores(self):
        """Zeigt das Highscore-Fenster an"""
        parent = self.parent()
        if parent and hasattr(parent, 'buttons') and hasattr(parent.buttons, 'highscore_model'):
            from src.views.highscores_window import HighscoresWindow
            highscores_dialog = HighscoresWindow(parent.buttons.highscore_model, self)
            highscores_dialog.exec()
        
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