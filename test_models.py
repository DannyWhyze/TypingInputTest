import unittest
from unittest.mock import patch
import time
from src.models.main_model import MainModel

class TestMainModelTimer(unittest.TestCase):

    def setUp(self):
        self.model = MainModel()

    def test_one_minute_timer_setup(self):
        """Test, dass der Timer korrekt auf 1 Minute gesetzt wird"""
        result = self.model.set_timer(1)
        self.assertTrue(result)
        self.assertEqual(self.model.timer_duration, 60)  # 1 Minute = 60 Sekunden
        self.assertEqual(self.model.time_remaining, 60)
        self.assertFalse(self.model.timer_active)  # Timer wird durch set_timer nicht aktiviert

    def test_one_minute_timer_start(self):
        """Test, dass der Timer korrekt startet"""
        self.model.set_timer(1)
        result = self.model.start_timer()
        self.assertTrue(result)
        self.assertTrue(self.model.timer_active)

    def test_one_minute_timer_update(self):
        """Test, dass update_timer korrekt funktioniert"""
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

    def test_time_remaining_string(self):
        """Test, dass die verbleibende Zeit korrekt formatiert wird"""
        self.model.set_timer(1)
        self.assertEqual(self.model.get_time_remaining_str(), "01:00")
        
        self.model.time_remaining = 45
        self.assertEqual(self.model.get_time_remaining_str(), "00:45")
        
        self.model.time_remaining = 5
        self.assertEqual(self.model.get_time_remaining_str(), "00:05")

    def test_keystrokes_per_second(self):
        """Test, dass die Anschlagsrate korrekt berechnet wird"""
        # Timer auf 1 Minute setzen und starten
        self.model.set_timer(1)
        self.model.start_timer()
        
        # 10 Anschläge in 5 Sekunden simulieren
        self.model.time_remaining = 55  # 5 Sekunden vergangen
        self.model.elapsed_time = 5     # Diese Zeile hinzufügen!
        for _ in range(10):
            self.model.increment_keystrokes()
            
        # Sollte 2.0 Anschläge pro Sekunde ergeben
        self.assertEqual(self.model.get_keystrokes_per_second(), 2.0)

if __name__ == '__main__':
    unittest.main()