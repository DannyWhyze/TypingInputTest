from PyQt6.QtWidgets import QTextEdit, QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from src.models.statisticsModel import StatisticsModel

class InputField(QWidget):
    def __init__(self, model, target_text_widget, stats_model=None, placeholder_text="Tippe den obigen Text ab..."):
        """
        Erstellt ein Widget mit einem größeren Textfeld (Multiline).
        :param placeholder_text: Platzhaltertext für das Textfeld.
        """
        super().__init__()
        self.model = model  # Verweis auf MainModel
        self.target_text_widget = target_text_widget
        # StatisticsModel verwenden oder neu erstellen
        self.stats_model = stats_model if stats_model else StatisticsModel(model)
        
        self.layout = QVBoxLayout(self)
        # Keine Abstände im Layout
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Erstelle ein QTextEdit (Multiline-Textfeld)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(placeholder_text)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        self.layout.addWidget(self.text_edit)

        # Signal anbinden
        self.text_edit.textChanged.connect(self.on_text_changed)
        self.text_edit.keyPressEvent = self.key_press_event

        self.setLayout(self.layout)

        # Flag, um zu prüfen, ob der Countdown gestartet wurde
        self.countdown_started = False

    def on_text_changed(self):
        """Diese Methode wird bei jeder Textänderung aufgerufen"""
        if not self.countdown_started and self.model.timer_duration > 0:
            self.countdown_started = True
            self.model.start_timer()
            window = self.window()
            if hasattr(window, 'countdown'):
                window.countdown.start_timer()
            
            # Restart-Button aktivieren, sobald das Tippen beginnt
            if hasattr(window, 'restart_button'):
                window.restart_button.setEnabled(True)
        
        # Tastenanschläge zählen
        self.model.increment_keystrokes()
        
        # Eingabe mit dem Zieltext vergleichen und farblich markieren
        typed_text = self.text_edit.toPlainText()
        status_list = self.model.check_typing(typed_text)
        self.target_text_widget.update_colored_text(status_list)
        
        # Aktualisiere andere Widgets und maximale Tippgeschwindigkeit
        window = self.window()
        if hasattr(window, 'buttons') and hasattr(window.buttons, 'tip_info'):
            current_speed = self.model.get_keystrokes_per_second()
            window.buttons.tip_info.update_info()
            # Maximale Geschwindigkeit aktualisieren
            self.stats_model.update_max_speed(current_speed)

    def key_press_event(self, event):
        """Überwacht jeden einzelnen Tastendruck"""
        # Erkennung von Backspace
        is_backspace = event.key() == Qt.Key.Key_Backspace
        
        if is_backspace:
            self.stats_model.track_keystroke(None, None, is_backspace=True)
        else:
            # Normaler Tastendruck
            key_char = event.text()
            if key_char:  # Nur sichtbare Zeichen verarbeiten
                cursor_pos = self.text_edit.textCursor().position()
                # Zielzeichen an dieser Position ermitteln
                target_text = self.target_text_widget.toPlainText()
                if cursor_pos < len(target_text):
                    target_char = target_text[cursor_pos]
                    # Zeichen tracken
                    self.stats_model.track_keystroke(key_char, target_char)
        
        # Standard-Ereignisverarbeitung nicht blockieren
        QTextEdit.keyPressEvent(self.text_edit, event)

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