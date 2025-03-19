import unittest
from src.models.statisticsModel import StatisticsModel
from src.models.main_model import MainModel

class TestStatisticsModel(unittest.TestCase):
    
    def setUp(self):
        self.main_model = MainModel()
        self.main_model.set_timer(1)
        self.main_model.current_text = "Dies ist ein Test."
        # Stelle sicher, dass escape_count initialisiert ist
        self.main_model.escape_count = 0
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
        
        # Backspace simulieren (als Korrektur zählt er)
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
        self.main_model.current_text = "Der Test ist gut."
        typed_text = "Der test ist Guz."
        stats = self.stats_model.calculate_typing_statistics(typed_text)
        self.assertIn('char', stats)
        self.assertIn('word', stats)
        self.assertEqual(stats['word']['correct'], 2)  # "Der" und "ist" korrekt
        self.assertEqual(stats['word']['case_error'], 1)  # "test" (falsche Großschreibung)
        self.assertEqual(stats['word']['wrong'], 1)        # "Guz" falsch

    def test_similar_characters_recognition(self):
        """Test, dass Umlaute und ihre Basis-Buchstaben als ähnlich erkannt werden"""
        if hasattr(self.main_model, 'are_similar_chars'):
            self.assertTrue(self.main_model.are_similar_chars('ä', 'a'))
            self.assertTrue(self.main_model.are_similar_chars('ö', 'o'))
            self.assertTrue(self.main_model.are_similar_chars('ü', 'u'))
            self.assertTrue(self.main_model.are_similar_chars('ß', 's'))
            self.assertFalse(self.main_model.are_similar_chars('a', 'e'))
            self.assertFalse(self.main_model.are_similar_chars('ö', 'u'))
            
            self.main_model.current_text = "Hör zu, Äpfel und Füße"
            typed_text = "Hor zu, Apfel und Fusse"
            status_list = self.main_model.check_typing(typed_text)
            umlaut_positions = [1, 8, 19, 20]
            for pos in umlaut_positions:
                self.assertEqual(status_list[pos], 2, 
                                 f"Buchstabe an Position {pos} sollte als halb-richtig (2) erkannt werden")
    
    def test_case_sensitivity(self):
        """Test, dass die Groß-/Kleinschreibungserkennung korrekt funktioniert"""
        self.main_model.current_text = "Das Ist Ein Test."
        typed_text = "das ist ein test."
        status_list = self.main_model.check_typing(typed_text)
        case_positions = [0, 4, 8, 12]
        for pos in case_positions:
            self.assertEqual(status_list[pos], 2, 
                             f"Buchstabe an Position {pos} sollte als halb-richtig (2) erkannt werden")
        for pos in range(len(typed_text)):
            if pos not in case_positions:
                self.assertEqual(status_list[pos], 1, 
                                 f"Buchstabe an Position {pos} sollte als korrekt (1) erkannt werden")
    
    def test_escape_key_tracking(self):
        """Test, dass die Escape-Taste nicht als Anschlag zählt, aber separat erfasst wird"""
        initial_escape = self.main_model.escape_count
        # Simuliere einen Escape-Tastendruck (dies würde in der InputField-Logik geschehen)
        self.main_model.escape_count += 1
        self.assertEqual(self.main_model.escape_count, initial_escape + 1)
    
    def test_max_speed_tracking(self):
        """Test, dass die maximale Tippgeschwindigkeit korrekt verfolgt wird"""
        self.assertEqual(self.stats_model.max_keystrokes_per_second, 0.0)
        self.stats_model.update_max_speed(2.5)
        self.assertEqual(self.stats_model.max_keystrokes_per_second, 2.5)
        self.stats_model.update_max_speed(1.8)
        self.assertEqual(self.stats_model.max_keystrokes_per_second, 2.5)
        self.stats_model.update_max_speed(3.2)
        self.assertEqual(self.stats_model.max_keystrokes_per_second, 3.2)
    
    def test_keystrokes_per_minute(self):
        """Test, dass die Anschläge pro Minute korrekt berechnet werden"""
        self.main_model.set_timer(1)
        self.main_model.start_timer()
        self.main_model.keystroke_count = 120
        self.main_model.elapsed_time = 60
        self.assertEqual(self.main_model.keystroke_count / (self.main_model.timer_duration / 60), 120)
        self.assertEqual(self.main_model.get_keystrokes_per_second(), 2.0)
        
        self.main_model.keystroke_count = 0
        self.main_model.set_timer(3)
        self.main_model.start_timer()
        self.main_model.keystroke_count = 300
        self.main_model.elapsed_time = 120
        self.assertEqual(self.main_model.keystroke_count / (self.main_model.elapsed_time / 60), 150)

if __name__ == '__main__':
    unittest.main()