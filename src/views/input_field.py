from PyQt6.QtWidgets import QTextEdit, QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

class InputField(QWidget):
    def __init__(self, model, placeholder_text="Enter your text here"):
        """
        Erstellt ein Widget mit einem größeren Textfeld (Multiline).
        :param placeholder_text: Platzhaltertext für das Textfeld.
        """
        super().__init__()
        self.model = model  # Verweis auf MainModel
        self.layout = QVBoxLayout(self)
        # Keine Abstände im Layout
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Erstelle ein QTextEdit (Multiline-Textfeld)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(placeholder_text)
        self.text_edit.setStyleSheet("font-size: 14px; padding: 5px;")
        self.text_edit.setFixedHeight(100)  # Höhe für ca. 4 Zeilen Text
        self.layout.addWidget(self.text_edit)

        # Signal anbinden
        self.text_edit.textChanged.connect(self.on_text_changed)

        self.setLayout(self.layout)

        # Flag, um zu prüfen, ob der Countdown gestartet wurde
        self.countdown_started = False

    def on_text_changed(self):
        """Diese Methode wird bei jeder Textänderung aufgerufen"""
        self.model.increment_keystrokes()
        
        # MainWindow finden
        window = self.window()
        
        # Timer starten beim ersten Tastendruck, wenn Timer vorbereitet ist
        if self.model.timer_duration > 0 and not self.model.timer_active:
            self.model.start_timer()  # Jetzt erst aktivieren
            if hasattr(window, 'countdown'):
                window.countdown.start_timer()
        
        # Tippinfo aktualisieren
        if hasattr(window, 'buttons') and hasattr(window.buttons, 'tip_info'):
            window.buttons.tip_info.update_info()

    def start_countdown(self):
        """Startet den Countdown im Hauptfenster."""
        window = self.window()
        if hasattr(window, 'countdown'):
            window.countdown.start_timer()

    def get_text(self):
        """
        Gibt den aktuellen Text im Textfeld zurück.
        :return: Der eingegebene Text als String.
        """
        return self.text_edit.toPlainText()

    def clear_text(self):
        """
        Löscht den Inhalt des Textfelds.
        """
        self.text_edit.clear()