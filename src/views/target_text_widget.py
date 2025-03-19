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
    
    def update_colored_text(self, status_list):
        """
        Aktualisiert den Text mit Farbformatierung:
        - Grün: Korrekt getippte Zeichen
        - Gelb: Falsche Groß-/Kleinschreibung
        - Rot: Falsche Buchstaben
        """
        # Formatierungen definieren
        correct_format = QTextCharFormat()
        correct_format.setForeground(QColor("green"))
        
        case_format = QTextCharFormat()
        case_format.setForeground(QColor("orange"))  # Gelb/Orange für Groß-/Kleinschreibungsfehler
        
        error_format = QTextCharFormat()
        error_format.setForeground(QColor("red"))
        
        normal_format = QTextCharFormat()
        normal_format.setForeground(QColor("black"))
        
        # Text formatieren
        cursor = self.textCursor()
        
        # Zuerst alles auf normale Formatierung setzen
        cursor.setPosition(0)
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
        cursor.setCharFormat(normal_format)
        
        # Dann jedes Zeichen entsprechend formatieren
        text = self.toPlainText()
        
        for i, status in enumerate(status_list):
            if i >= len(text):
                break
                
            cursor.setPosition(i)
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)
            
            if status == 1:  # Korrekt
                cursor.setCharFormat(correct_format)
            elif status == 2:  # Falsche Groß-/Kleinschreibung
                cursor.setCharFormat(case_format)
            elif status == 3:  # Falscher Buchstabe
                cursor.setCharFormat(error_format)
            # Status 0 bleibt schwarz (unformatiert)
        
        # Auto-Scrolling
        correct_count = status_list.count(1)  # Anzahl korrekter Zeichen für Scrolling
        self.check_and_scroll(correct_count)

    def check_and_scroll(self, correct_count):
        """
        Überprüft, ob gescrollt werden muss und führt das Scrolling aus.
        Scrollt, wenn 75% des sichtbaren Bereichs getippt wurden.
        """
        # Prüfen, ob wir bereits am Ende des Textes sind
        if correct_count >= len(self.toPlainText()):
            return
        
        # Position des letzten korrekt getippten Zeichens ermitteln
        cursor = self.textCursor()
        cursor.setPosition(correct_count)
        
        # Rechteck für die aktuelle Cursor-Position holen
        cursor_rect = self.cursorRect(cursor)
        
        # Sichtbaren Bereich holen
        viewport_height = self.viewport().height()
        
        # Wenn der Cursor im unteren Viertel des sichtbaren Bereichs ist, scrollen
        if cursor_rect.bottom() > viewport_height * 0.75:
            # Neue Scrollposition berechnen (cursor in oberes Viertel)
            new_scroll_value = self.verticalScrollBar().value() + (cursor_rect.bottom() - viewport_height * 0.25)
            
            # Scrollen
            self.verticalScrollBar().setValue(int(new_scroll_value))