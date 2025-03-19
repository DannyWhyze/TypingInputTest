from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QTextCharFormat, QColor, QTextCursor

class TargetTextWidget(QTextEdit):
    def __init__(self, model):
        super().__init__()
        self.model = model
        
        # Widget-Einstellungen
        self.setReadOnly(True)  # Nur Anzeige, keine Eingabe
        self.setStyleSheet("""
            QTextEdit {
                background-color: #f8f8f8;
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        
        # Initial Text generieren
        self.refresh_text()
        
    def refresh_text(self):
        """Generiert neuen Text und zeigt ihn an."""
        text = self.model.generate_text_for_typing(200)  # Statt Standardwert (20) explizit 100 Wörter anfordern
        self.setPlainText(text)
    
    def update_colored_text(self, correct_count):
        """
        Aktualisiert den Text und markiert die korrekten Zeichen grün.
        """
        # Formatierung für korrekte Zeichen
        correct_format = QTextCharFormat()
        correct_format.setForeground(QColor("green"))
        
        # Formatierung für noch nicht getippte Zeichen
        normal_format = QTextCharFormat()
        normal_format.setForeground(QColor("black"))
        
        # Text setzen und Cursor positionieren
        cursor = self.textCursor()
        cursor.setPosition(0)
        
        # Zuerst den gesamten Text auf normale Formatierung setzen
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
        cursor.setCharFormat(normal_format)
        
        # Dann die korrekten Zeichen grün markieren
        if correct_count > 0:
            cursor.setPosition(0)
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, correct_count)
            cursor.setCharFormat(correct_format)