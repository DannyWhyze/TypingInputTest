from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QTextCharFormat, QColor, QSyntaxHighlighter
from PyQt6.QtCore import Qt

class TypingHighlighter(QSyntaxHighlighter):
    def __init__(self, document, model):
        super().__init__(document)
        self.model = model
        self.status_list = []
        
    def set_status_list(self, status_list):
        """Aktualisiert die Status-Liste und triggert Neuformatierung"""
        self.status_list = status_list
        self.rehighlight()  # Löst Neuformatierung aus
        
    def get_format(self, color):
        """Erstellt ein QTextCharFormat mit der angegebenen Farbe"""
        text_format = QTextCharFormat()
        text_format.setForeground(QColor(color))
        return text_format
        
    def highlightBlock(self, text):
        """Formatiert den aktuellen Textblock"""
        # Diese Methode wird automatisch für sichtbare Textblöcke aufgerufen
        start_pos = self.currentBlock().position()
        
        # Formatierungen für verschiedene Status vorbereiten
        formats = [
            QTextCharFormat(),              # Schwarz (noch nicht getippt)
            self.get_format("green"),       # Grün (korrekt)
            self.get_format("orange"),      # Orange (halb-richtig)
            self.get_format("red")          # Rot (falsch)
        ]
        
        # Nur Zeichen formatieren, für die ein Status existiert
        for i, char in enumerate(text):
            pos = start_pos + i
            if pos < len(self.status_list):
                self.setFormat(i, 1, formats[self.status_list[pos]])


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
        
        # Syntax-Highlighter initialisieren
        self.highlighter = TypingHighlighter(self.document(), self.model)
        
        # Initial Text generieren
        self.refresh_text()
        
    def refresh_text(self):
        """Generiert neuen Text und zeigt ihn an."""
        text = self.model.generate_text_for_typing(200)  # 200 Wörter anfordern
        self.setPlainText(text)
    
    def update_colored_text(self, status_list):
        """
        Aktualisiert die Textformatierung basierend auf der Status-Liste
        Verwendet den Highlighter für effiziente Formatierung
        """
        # Status-Liste im Highlighter aktualisieren
        self.highlighter.set_status_list(status_list)
        
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