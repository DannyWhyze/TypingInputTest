import unittest
from unittest.mock import patch
import time
from src.models.main_model import MainModel

class TestMainModelTimer(unittest.TestCase):

    def setUp(self):
        self.model = MainModel()

    # Tests für 1-Minuten-Timer
    def test_one_minute_timer_setup(self):
        """Test, dass der Timer korrekt auf 1 Minute gesetzt wird"""
        result = self.model.set_timer(1)
        self.assertTrue(result)
        self.assertEqual(self.model.timer_duration, 60)  # 1 Minute = 60 Sekunden
        self.assertEqual(self.model.time_remaining, 60)
        self.assertFalse(self.model.timer_active)  # Timer wird durch set_timer nicht aktiviert

    def test_one_minute_timer_start(self):
        """Test, dass der 1-Minuten-Timer korrekt startet"""
        self.model.set_timer(1)
        result = self.model.start_timer()
        self.assertTrue(result)
        self.assertTrue(self.model.timer_active)

    def test_one_minute_timer_update(self):
        """Test, dass update_timer beim 1-Minuten-Timer korrekt funktioniert"""
        self.model.set_timer(1)
        self.model.start_timer()
        
        # Erster Update sollte eine Sekunde abziehen
        result = self.model.update_timer()
        self.assertTrue(result)
        self.assertEqual(self.model.time_remaining, 59)
        self.assertEqual(self.model.elapsed_time, 1)
        
        # Manuelles Setzen auf fast abgelaufen
        self.model.time_remaining = 1
        result = self.model.update_timer()
        self.assertTrue(result)
        self.assertEqual(self.model.time_remaining, 0)
        
        # Timer sollte nach Ablauf deaktiviert werden
        result = self.model.update_timer()
        self.assertFalse(result)
        self.assertFalse(self.model.timer_active)

    # Tests für 3-Minuten-Timer
    def test_three_minute_timer_setup(self):
        """Test, dass der Timer korrekt auf 3 Minuten gesetzt wird"""
        result = self.model.set_timer(3)
        self.assertTrue(result)
        self.assertEqual(self.model.timer_duration, 180)  # 3 Minuten = 180 Sekunden
        self.assertEqual(self.model.time_remaining, 180)
        self.assertFalse(self.model.timer_active)  # Timer wird durch set_timer nicht aktiviert

    def test_three_minute_timer_start(self):
        """Test, dass der 3-Minuten-Timer korrekt startet"""
        self.model.set_timer(3)
        result = self.model.start_timer()
        self.assertTrue(result)
        self.assertTrue(self.model.timer_active)

    def test_three_minute_timer_update(self):
        """Test, dass update_timer beim 3-Minuten-Timer korrekt funktioniert"""
        self.model.set_timer(3)
        self.model.start_timer()
        
        # Erster Update sollte eine Sekunde abziehen
        result = self.model.update_timer()
        self.assertTrue(result)
        self.assertEqual(self.model.time_remaining, 179)
        self.assertEqual(self.model.elapsed_time, 1)
        
        # Weitere Updates testen
        for _ in range(9):  # 9 weitere Updates für insgesamt 10 Sekunden
            result = self.model.update_timer()
            self.assertTrue(result)
        
        self.assertEqual(self.model.time_remaining, 170)  # 180 - 10 Sekunden
        self.assertEqual(self.model.elapsed_time, 10)

    # Tests für 5-Minuten-Timer
    def test_five_minute_timer_setup(self):
        """Test, dass der Timer korrekt auf 5 Minuten gesetzt wird"""
        result = self.model.set_timer(5)
        self.assertTrue(result)
        self.assertEqual(self.model.timer_duration, 300)  # 5 Minuten = 300 Sekunden
        self.assertEqual(self.model.time_remaining, 300)
        self.assertFalse(self.model.timer_active)  # Timer wird durch set_timer nicht aktiviert

    def test_five_minute_timer_start(self):
        """Test, dass der 5-Minuten-Timer korrekt startet"""
        self.model.set_timer(5)
        result = self.model.start_timer()
        self.assertTrue(result)
        self.assertTrue(self.model.timer_active)

    def test_five_minute_timer_update(self):
        """Test, dass update_timer beim 5-Minuten-Timer korrekt funktioniert"""
        self.model.set_timer(5)
        self.model.start_timer()
        
        # Erster Update sollte eine Sekunde abziehen
        result = self.model.update_timer()
        self.assertTrue(result)
        self.assertEqual(self.model.time_remaining, 299)
        self.assertEqual(self.model.elapsed_time, 1)
        
        # Weitere Updates testen
        for _ in range(29):  # 29 weitere Updates für insgesamt 30 Sekunden
            result = self.model.update_timer()
            self.assertTrue(result)
        
        self.assertEqual(self.model.time_remaining, 270)  # 300 - 30 Sekunden
        self.assertEqual(self.model.elapsed_time, 30)

    # Gemeinsame Tests für die Zeitformatierung und Anschlagsberechnung
    def test_time_remaining_string(self):
        """Test, dass die verbleibende Zeit korrekt formatiert wird"""
        self.model.set_timer(1)
        self.assertEqual(self.model.get_time_remaining_str(), "01:00")
        
        self.model.time_remaining = 45
        self.assertEqual(self.model.get_time_remaining_str(), "00:45")
        
        self.model.time_remaining = 5
        self.assertEqual(self.model.get_time_remaining_str(), "00:05")
        
        # Auch für längere Zeiten testen
        self.model.time_remaining = 185
        self.assertEqual(self.model.get_time_remaining_str(), "03:05")

    def test_keystrokes_per_second(self):
        """Test, dass die Anschlagsrate korrekt berechnet wird"""
        # Timer auf 1 Minute setzen und starten
        self.model.set_timer(1)
        self.model.start_timer()
        
        # 10 Anschläge in 5 Sekunden simulieren
        self.model.time_remaining = 55  # 5 Sekunden vergangen
        self.model.elapsed_time = 5     
        for _ in range(10):
            self.model.increment_keystrokes()
            
        # Sollte 2.0 Anschläge pro Sekunde ergeben
        self.assertEqual(self.model.get_keystrokes_per_second(), 2.0)
        
        # Nochmal mit verschiedenen Werten testen
        self.model.keystroke_count = 0
        self.model.time_remaining = 30  # 30 Sekunden vergangen
        self.model.elapsed_time = 30
        
        for _ in range(90):  # 90 Anschläge
            self.model.increment_keystrokes()
            
        self.assertEqual(self.model.get_keystrokes_per_second(), 3.0)

if __name__ == '__main__':
    unittest.main()