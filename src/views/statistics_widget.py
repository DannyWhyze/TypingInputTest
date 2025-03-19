from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class StatisticsWidget(QWidget):
    def __init__(self, statistics, stats_model):
        """
        Erstellt ein Widget zur tabellarischen Anzeige der Tippstatistik.
        :param statistics: Dictionary mit den Tippstatistiken
        :param stats_model: Referenz zum StatisticsModel für zusätzliche Infos
        """
        super().__init__()
        self.statistics = statistics
        self.stats_model = stats_model
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(15)
        
        # Grid für die Tabelle
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(10)
        
        # Tabelle erstellen und hinzufügen
        self.create_statistics_table()
        self.main_layout.addWidget(self.grid_widget)
        
        # Fußnoten und zusätzliche Informationen
        self.add_footnotes()
        
    def create_statistics_table(self):
        """Erstellt eine tabellarische Darstellung der Tippstatistik."""
        # 1. Überschriften
        header_font = QFont()
        header_font.setBold(True)
        
        # Tabellen-Header (Spaltenüberschriften)
        empty_label = QLabel("")
        self.grid_layout.addWidget(empty_label, 0, 0)
        
        headers = ["Richtig", "Halb-richtig(*)", "Falsch"]  # (*) hinzugefügt
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setFont(header_font)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(f"color: {'green' if col==0 else 'orange' if col==1 else 'red'};")
            self.grid_layout.addWidget(label, 0, col+1)
        
        # 2. Zeilen-Header
        row_headers = ["Zeichen:", "Wörter:"]
        for row, header in enumerate(row_headers):
            label = QLabel(header)
            label.setFont(header_font)
            label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.grid_layout.addWidget(label, row+1, 0)
        
        # 3. Daten einfügen
        # Zeichen-Statistik - endgültiger Status
        char_stats = self.statistics['char']
        self.add_data_cell(1, 1, char_stats['correct'], "green")
        self.add_data_cell(1, 2, char_stats['case_error'], "orange")
        self.add_data_cell(1, 3, char_stats['wrong'], "red")
        
        # Zusätzliche Zeile für Gesamtstatistik hinzufügen
        self.add_header_row(3, "Gesamt getippt:")
        self.add_data_cell(3, 1, char_stats['total_correct'], "green")
        self.add_data_cell(3, 2, char_stats['total_case_error'], "orange")
        self.add_data_cell(3, 3, char_stats['total_wrong'], "red")
        
        # Zusätzliche Information für Backspace-Nutzung und Fehlerrate
        self.add_info_row(4, f"Verwendete Backspaces: {char_stats['backspaces']}")
        self.add_info_row(5, f"Fehlerrate: {char_stats['error_rate']}%")
        
        # Wort-Statistik
        word_stats = self.statistics['word']
        self.add_data_cell(2, 1, word_stats['correct'], "green")
        self.add_data_cell(2, 2, word_stats['case_error'], "orange")
        self.add_data_cell(2, 3, word_stats['wrong'], "red")
        
        # Spaltenbreite anpassen
        self.grid_layout.setColumnStretch(0, 0)
        for i in range(1, 4):
            self.grid_layout.setColumnStretch(i, 1)
    
    def add_data_cell(self, row, col, value, color):
        label = QLabel(str(value))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {color};
            background-color: rgba({','.join(map(str, self.get_rgba_for_color(color)))});
            padding: 5px;
            border-radius: 3px;
        """)
        self.grid_layout.addWidget(label, row, col)
        
    def get_rgba_for_color(self, color):
        """Gibt RGBA-Werte für die Hintergrundfarbe zurück (leicht transparent)"""
        if color == "green":
            return (76, 175, 80, 30)  # Hellgrün (30% Opazität)
        elif color == "orange":
            return (255, 152, 0, 30)  # Hellorange (30% Opazität)
        elif color == "red":
            return (244, 67, 54, 30)  # Hellrot (30% Opazität)
        return (255, 255, 255, 0)  # Transparent

    def add_header_row(self, row, text):
        """Fügt eine Überschriftenzeile hinzu"""
        header_font = QFont()
        header_font.setBold(True)
        label = QLabel(text)
        label.setFont(header_font)
        label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(label, row, 0)

    def add_info_row(self, row, text):
        """Fügt eine Informationszeile hinzu"""
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setStyleSheet("font-size: 14px; padding: 5px;")
        # Eine Info, die über alle Spalten geht
        self.grid_layout.addWidget(label, row, 0, 1, 4)

    def add_footnotes(self):
        """Fügt Fußnoten und zusätzliche Informationen unter der Tabelle hinzu"""
        # Erklärung für Halb-richtig
        footnote = QLabel("(*) Halb-richtig = Umlaut/Großbuchstabe wurde nicht ganz richtig geschrieben (\"a\" statt \"A\" oder \"o\" statt \"ö\")")
        footnote.setWordWrap(True)
        footnote.setStyleSheet("font-size: 12px; font-style: italic; color: #666;")
        self.main_layout.addWidget(footnote)
        
        # Kleiner Abstand
        self.main_layout.addSpacing(5)
        
        # Zeile für Korrekturen
        corrections = QLabel(f"Es wurden insgesamt {self.statistics['char']['backspaces']} Korrekturen durchgeführt.")
        corrections.setStyleSheet("font-size: 13px;")
        self.main_layout.addWidget(corrections)
        
        # Zeile für maximale Tippgeschwindigkeit
        max_speed = QLabel(f"Die maximale Tippgeschwindigkeit betrug {self.stats_model.max_keystrokes_per_second} Zeichen in der Sekunde.")
        max_speed.setStyleSheet("font-size: 13px;")
        self.main_layout.addWidget(max_speed)