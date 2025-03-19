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
        """Erstellt das Help-Menü (vorerst leer)"""
        self.addMenu("&Help")
    
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