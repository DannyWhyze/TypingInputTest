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
        self.model = model  # Referenz auf MainModel
        self.target_text_widget = target_text_widget
        # StatisticsModel verwenden oder neu erstellen
        self.stats_model = stats_model if stats_model else StatisticsModel(model)
        # Variable, um Escape-Nutzung zu zählen (nicht als Anschlag)
        self.stats_model.escape_count = 0
        
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
        # Überschreibe die KeyPress-Event-Methode
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
        
        # Normalerweise wird bei jedem gültigen Anschlag die Anzahl erhöht; 
        # dies geschieht nun in key_press_event
        typed_text = self.text_edit.toPlainText()
        status_list = self.model.check_typing(typed_text)
        self.target_text_widget.update_colored_text(status_list)
        
        window = self.window()
        if hasattr(window, 'buttons') and hasattr(window.buttons, 'tip_info'):
            current_speed = self.model.get_keystrokes_per_second()
            window.buttons.tip_info.update_info()
            self.stats_model.update_max_speed(current_speed)

    def key_press_event(self, event):
        """Überwacht jeden einzelnen Tastendruck und zählt nur sichtbare, buchstabenproduzierende Zeichen."""
        key = event.key()
        # Definition der zu ignorierenden Tasten:
        ignore_keys = {
            Qt.Key.Key_Shift, Qt.Key.Key_Control, Qt.Key.Key_Alt,
            Qt.Key.Key_AltGr, Qt.Key.Key_CapsLock, Qt.Key.Key_Meta
        }
        # Sonderfälle: Enter nicht als Anschlag zählen; Pfeiltasten, Tab ignorieren
        navigation_keys = {
            Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up,
            Qt.Key.Key_Down, Qt.Key.Key_Tab
        }
        
        if key in ignore_keys:
            QTextEdit.keyPressEvent(self.text_edit, event)
            return
        
        if key in {Qt.Key.Key_Enter, Qt.Key.Key_Return}:
            QTextEdit.keyPressEvent(self.text_edit, event)
            return

        if key in {Qt.Key.Key_Backspace, Qt.Key.Key_Delete}:
            # Backspace und Delete führen zur Korrektur (mit separater Zählung)
            self.stats_model.track_keystroke(None, None, is_backspace=True)
            QTextEdit.keyPressEvent(self.text_edit, event)
            return
        
        if key in navigation_keys:
            QTextEdit.keyPressEvent(self.text_edit, event)
            return
        
        if key == Qt.Key.Key_Escape:
            # Escape zählt nicht als Anschlag, wird jedoch separat getrackt.
            self.stats_model.escape_count += 1
            QTextEdit.keyPressEvent(self.text_edit, event)
            return
        
        # Normale Zeichen: Anschlag soll gezählt werden
        self.model.increment_keystrokes()
        key_char = event.text()
        if key_char:  # Nur sichtbare Zeichen verarbeiten
            cursor_pos = self.text_edit.textCursor().position()
            target_text = self.target_text_widget.toPlainText()
            if cursor_pos < len(target_text):
                target_char = target_text[cursor_pos]
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