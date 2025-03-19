from PyQt6.QtWidgets import QTextEdit, QWidget, QVBoxLayout

class InputField(QWidget):
    def __init__(self, placeholder_text="Enter your text here"):
        """
        Erstellt ein Widget mit einem größeren Textfeld (Multiline).
        :param placeholder_text: Platzhaltertext für das Textfeld.
        """
        super().__init__()
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

        self.setLayout(self.layout)

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