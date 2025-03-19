from PyQt6.QtWidgets import QMenuBar, QMenu, QMessageBox
from PyQt6.QtGui import QAction
from src.views.highscores_window import HighscoresWindow

class ApplicationMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Styling für die Menüleiste
        self.setStyleSheet("""
            QMenuBar {
                background-color: #2c3e50;
                color: white;
                padding: 5px;
                font-weight: bold;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
                margin: 0px 2px;
                border-radius: 3px;
            }
            QMenuBar::item:selected {
                background-color: #3498db;
            }
            QMenuBar::item:pressed {
                background-color: #2980b9;
            }
            QMenu {
                background-color: #34495e;
                color: white;
                border: 1px solid #2c3e50;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 30px 5px 20px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #3498db;
            }
        """)
        
        # Menüs erstellen
        self.create_file_menu()
        self.create_edit_menu()
        self.create_help_menu()
        
    def create_file_menu(self):
        """Erstellt das File-Menü"""
        file_menu = self.addMenu("&File")
        
        # Neu starten Aktion
        restart_action = QAction("Neu starten", self)
        restart_action.triggered.connect(self.restart_game)
        file_menu.addAction(restart_action)
        
        # Highscore anzeigen Aktion
        show_highscores_action = QAction("Highscores anzeigen", self)
        show_highscores_action.triggered.connect(self.show_highscores)
        file_menu.addAction(show_highscores_action)
        
        # Trenner
        file_menu.addSeparator()
        
        # Beenden-Aktion
        exit_action = QAction("Beenden", self)
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)
    
    def create_edit_menu(self):
        """Erstellt das Edit-Menü"""
        edit_menu = self.addMenu("&Edit")
        
        # Highscore löschen Aktion
        clear_highscores_action = QAction("Highscores löschen", self)
        clear_highscores_action.triggered.connect(self.clear_highscores)
        edit_menu.addAction(clear_highscores_action)
    
    def create_help_menu(self):
        """Erstellt das Help-Menü mit Punkteregeln und About-Infos"""
        help_menu = self.addMenu("&Help")
        
        # Punkteregeln-Aktion
        rules_action = QAction("Regeln der Punktevergabe", self)
        rules_action.triggered.connect(self.show_score_rules)
        help_menu.addAction(rules_action)
        
        # Trenner
        help_menu.addSeparator()
        
        # About-Aktion
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_highscores(self):
        """Zeigt das Highscore-Fenster an"""
        # Highscore-Model von ButtonsUI verwenden, falls bereits initialisiert
        if hasattr(self.parent, 'buttons') and hasattr(self.parent.buttons, 'highscore_model'):
            highscores_dialog = HighscoresWindow(self.parent.buttons.highscore_model, self.parent)
            highscores_dialog.exec()
        else:
            # Falls das Fenster vor der ButtonsUI-Initialisierung geöffnet wird
            from src.models.highscore_model import HighscoreModel
            highscore_model = HighscoreModel()
            highscores_dialog = HighscoresWindow(highscore_model, self.parent)
            highscores_dialog.exec()
    
    def clear_highscores(self):
        """Löscht alle Highscores nach Bestätigung"""
        # Sicherheitsabfrage
        confirm = QMessageBox.question(
            self.parent, 
            "Highscores löschen", 
            "Möchtest du wirklich alle Highscores löschen? Diese Aktion kann nicht rückgängig gemacht werden.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            # Highscores löschen
            if hasattr(self.parent, 'buttons') and hasattr(self.parent.buttons, 'highscore_model'):
                self.parent.buttons.highscore_model.highscores = []
                self.parent.buttons.highscore_model.save_highscores()
                QMessageBox.information(self.parent, "Erfolg", "Alle Highscores wurden gelöscht.")
            else:
                QMessageBox.warning(self.parent, "Fehler", "Highscores konnten nicht gelöscht werden.")

    def restart_game(self):
        """Startet das Spiel neu"""
        if hasattr(self.parent, 'reset_for_new_test'):
            self.parent.reset_for_new_test()

    def show_score_rules(self):
        """Zeigt ein Dialogfenster mit den Regeln der Punktevergabe"""
        rules_text = """
        <h2>Regeln der Punktevergabe</h2>
        
        <h3>Basispunkte:</h3>
        <ul>
            <li>+1 Punkt für jeden korrekt getippten Buchstaben (grün)</li>
        </ul>
        
        <h3>Abzüge:</h3>
        <ul>
            <li>-1 Punkt für jedes halb-richtige Wort (gelb)</li>
            <li>-2 Punkte für jedes falsche Wort (rot)</li>
            <li>-2 Punkte für jedes Wort mit gemischten Fehlern (gelb und rot)</li>
            <li>-1 Punkt pro Backspace</li>
        </ul>
        
        <h3>Boni:</h3>
        <ul>
            <li>+0,5 Punkte pro erfolgreiche Korrektur</li>
            <li>+50 Punkte für 10 fehlerfreie Wörter in Folge</li>
            <li>Geschwindigkeitsbonus:
                <ul>
                    <li>+100 Punkte bei 60+ Anschlägen pro Minute</li>
                    <li>+250 Punkte bei 80+ Anschlägen pro Minute</li>
                    <li>+500 Punkte bei 100+ Anschlägen pro Minute</li>
                </ul>
            </li>
            <li>+200 Punkte für gleichmäßiges Tippen</li>
        </ul>
        
        <h3>Schwierigkeitsgrade:</h3>
        <ul>
            <li>1-Minute-Test: Faktor 1.0</li>
            <li>3-Minuten-Test: Faktor 1.1</li>
            <li>5-Minuten-Test: Faktor 1.2</li>
        </ul>

        <h3>Nicht gezählte Tasten:</h3>
        <p>Folgende Tasten werden nicht als Anschläge gezählt:</p>
        <ul>
            <li><strong>Modifiziertasten:</strong> Shift, Strg (Ctrl), Alt, AltGr, Caps Lock, Windows-Taste, Fn</li>
            <li><strong>Enter/Return:</strong> Erzeugt zwar einen Zeilenumbruch, zählt aber nicht als Anschlag</li>
            <li><strong>Navigationstasten:</strong> Pfeiltasten (links, rechts, oben, unten), Tab</li>
            <li><strong>Escape:</strong> Wird separat erfasst, aber nicht als Anschlag gezählt</li>
            <li><strong>Backspace und Delete:</strong> Werden als Korrekturen gezählt, nicht als Anschläge</li>
        </ul>
        """
        
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser
        from PyQt6.QtCore import Qt
        
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Regeln der Punktevergabe")
        dialog.setMinimumSize(500, 650)  # Etwas größer für den zusätzlichen Inhalt
        
        layout = QVBoxLayout(dialog)
        text_browser = QTextBrowser()
        text_browser.setHtml(rules_text)
        text_browser.setOpenExternalLinks(True)
        layout.addWidget(text_browser)
        
        dialog.exec()

    def show_about(self):
        """Zeigt ein Dialogfenster mit About-Informationen"""
        about_text = """
        <div style="text-align: center; margin: 20px;">
            <h2>Typing Test</h2>
            <h3>Version 1.0</h3>
            <p>Entwickelt von: Danny Whyze</p>
            <p>Organisation: Bars2Bars</p>
        </div>
        """
        
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser
        from PyQt6.QtCore import Qt
        
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("About")
        dialog.setFixedSize(300, 200)
        
        layout = QVBoxLayout(dialog)
        text_browser = QTextBrowser()
        text_browser.setHtml(about_text)
        text_browser.setOpenExternalLinks(True)
        layout.addWidget(text_browser)
        
        dialog.exec()