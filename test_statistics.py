import unittest
from src.models.statisticsModel import StatisticsModel
from src.models.main_model import MainModel

class TestStatisticsModel(unittest.TestCase):
    
    def setUp(self):
        self.main_model = MainModel()
        self.main_model.set_timer(1)
        self.main_model.current_text = "Dies ist ein Test."
        self.stats_model = StatisticsModel(self.main_model)
    
    def test_keystroke_tracking(self):
        """Test, dass Tastenanschläge korrekt erfasst werden"""
        # Korrekte Tastenanschläge
        self.stats_model.track_keystroke("D", "D")
        self.stats_model.track_keystroke("i", "i")
        
        # Falsche Groß-/Kleinschreibung
        self.stats_model.track_keystroke("e", "E")
        
        # Falscher Buchstabe
        self.stats_model.track_keystroke("x", "s")
        
        # Backspace
        self.stats_model.track_keystroke(None, None, is_backspace=True)
        
        # Überprüfung der Zähler
        self.assertEqual(self.stats_model.total_keystrokes, 4)
        self.assertEqual(self.stats_model.correct_keystrokes, 2)
        self.assertEqual(self.stats_model.case_error_keystrokes, 1)
        self.assertEqual(self.stats_model.wrong_keystrokes, 1)
        self.assertEqual(self.stats_model.backspaces, 1)
    
    def test_error_rate_calculation(self):
        """Test, dass die Fehlerrate korrekt berechnet wird"""
        # 20 Tastenanschläge, davon 2 fehlerhafte
        self.stats_model.total_keystrokes = 20
        self.stats_model.case_error_keystrokes = 1
        self.stats_model.wrong_keystrokes = 1
        
        # Fehlerrate sollte 10% sein (2/20)
        self.assertEqual(self.stats_model.calculate_error_rate(), 10.0)
    
    def test_typing_statistics_calculation(self):
        """Test zur Berechnung der Tippstatistiken"""
        # Setze Beispieltext
        self.main_model.current_text = "Der Test ist gut."
        
        # Simuliere einen getippten Text mit Fehlern
        typed_text = "Der test ist Guz."
        
        # Berechne Statistik
        stats = self.stats_model.calculate_typing_statistics(typed_text)
        
        # Überprüfe Charakter-Statistiken
        self.assertIn('char', stats)
        
        # Überprüfe Wort-Statistiken
        self.assertIn('word', stats)
        self.assertEqual(stats['word']['correct'], 2)  # "Der" und "ist" sind korrekt
        self.assertEqual(stats['word']['case_error'], 1)  # "test" hat falsche Großschreibung
        self.assertEqual(stats['word']['wrong'], 1)  # "Guz" ist falsch

    def test_similar_characters_recognition(self):
        """Test, dass Umlaute und ihre Basis-Buchstaben als ähnlich erkannt werden"""
        # Test für are_similar_chars direkt (falls verfügbar)
        if hasattr(self.main_model, 'are_similar_chars'):
            # Prüfe Umlaute und ihre Basis-Buchstaben
            self.assertTrue(self.main_model.are_similar_chars('ä', 'a'))
            self.assertTrue(self.main_model.are_similar_chars('ö', 'o'))
            self.assertTrue(self.main_model.are_similar_chars('ü', 'u'))
            self.assertTrue(self.main_model.are_similar_chars('ß', 's'))
            
            # Prüfe Groß-/Kleinschreibung bei Umlauten
            self.assertTrue(self.main_model.are_similar_chars('Ö', 'o'))
            self.assertTrue(self.main_model.are_similar_chars('ä', 'A'))
            
            # Prüfe, dass nicht-ähnliche Buchstaben als falsch erkannt werden
            self.assertFalse(self.main_model.are_similar_chars('a', 'e'))
            self.assertFalse(self.main_model.are_similar_chars('ö', 'u'))
        
        # Test für die Klassifizierung in check_typing
        self.main_model.current_text = "Hör zu, Äpfel und Füße"
        typed_text = "Hor zu, Apfel und Fusse"
        
        status_list = self.main_model.check_typing(typed_text)
        
        # Prüfe, ob die Umlaute als halb-richtig (2) erkannt werden
        # Positionen der Umlaute im Originaltext
        umlaut_positions = [1, 8, 19, 20]  # ö, Ä, ü, ß
        
        for pos in umlaut_positions:
            self.assertEqual(status_list[pos], 2, 
                            f"Buchstabe an Position {pos} sollte als halb-richtig (2) erkannt werden")

    def test_case_sensitivity(self):
        """Test, dass die Groß-/Kleinschreibungserkennung korrekt funktioniert"""
        self.main_model.current_text = "Das Ist Ein Test."
        typed_text = "das ist ein test."
        
        # Berechne Status-Liste
        status_list = self.main_model.check_typing(typed_text)
        
        # Position von Groß-/Kleinschreibungsfehlern
        case_positions = [0, 4, 8, 12]  # D -> d, I -> i, E -> e, T -> t
        
        # Prüfe, ob alle als Fehlertyp 2 (Groß-/Kleinschreibung) erkannt werden
        for pos in case_positions:
            self.assertEqual(status_list[pos], 2, 
                            f"Buchstabe an Position {pos} sollte als halb-richtig (2) erkannt werden")
        
        # Prüfe, ob der Rest korrekt ist (Typ 1)
        for pos in range(len(typed_text)):
            if pos not in case_positions:
                self.assertEqual(status_list[pos], 1, 
                                f"Buchstabe an Position {pos} sollte als korrekt (1) erkannt werden")

    def test_max_speed_tracking(self):
        """Test, dass die maximale Tippgeschwindigkeit korrekt verfolgt wird"""
        # Initial sollte die maximale Geschwindigkeit 0 sein
        self.assertEqual(self.stats_model.max_keystrokes_per_second, 0.0)
        
        # Aktualisieren mit verschiedenen Werten
        self.stats_model.update_max_speed(2.5)
        self.assertEqual(self.stats_model.max_keystrokes_per_second, 2.5)
        
        # Niedrigerer Wert sollte ignoriert werden
        self.stats_model.update_max_speed(1.8)
        self.assertEqual(self.stats_model.max_keystrokes_per_second, 2.5)
        
        # Höherer Wert sollte aktualisieren
        self.stats_model.update_max_speed(3.2)
        self.assertEqual(self.stats_model.max_keystrokes_per_second, 3.2)

    def test_keystrokes_per_minute(self):
        """Test für die Berechnung von Anschlägen pro Minute"""
        # 1-Minuten-Timer einrichten
        self.main_model.set_timer(1)
        self.main_model.start_timer()
        
        # 120 Tastenanschläge in einer Minute simulieren (genau 2 pro Sekunde)
        self.main_model.keystroke_count = 120
        self.main_model.elapsed_time = 60  # Volle Minute
        
        # Überprüfen der Anschläge pro Minute (sollte 120 sein)
        keystrokes_per_minute = self.main_model.keystroke_count / (self.main_model.timer_duration / 60)
        self.assertEqual(keystrokes_per_minute, 120)
        
        # Überprüfen der Anschläge pro Sekunde (sollte 2.0 sein)
        self.assertEqual(self.main_model.get_keystrokes_per_second(), 2.0)
        
        # Test mit 3-Minuten-Timer
        self.main_model.set_timer(3)
        self.main_model.start_timer()
        
        # 300 Anschläge in 2 Minuten
        self.main_model.keystroke_count = 300
        self.main_model.elapsed_time = 120  # 2 Minuten
        
        # Überprüfen der Anschläge pro Minute (sollte 150 sein: 300/2)
        keystrokes_per_minute = self.main_model.keystroke_count / (self.main_model.elapsed_time / 60)
        self.assertEqual(keystrokes_per_minute, 150)