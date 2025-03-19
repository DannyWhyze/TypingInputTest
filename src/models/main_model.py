class MainModel:
    def __init__(self):        
        self.keystroke_count = 0  # Zählt die Tastenanschläge
        
        # Timer-Attribute
        self.timer_duration = 0  # Dauer in Sekunden (0, 60, 180, 300)
        self.time_remaining = 0  # Verbleibende Zeit in Sekunden
        self.timer_active = False  # Gibt an, ob der Timer aktiv ist
    
    def increment_keystrokes(self):
        self.keystroke_count += 1
    
    def set_timer(self, minutes):
        """Setzt den Timer auf die angegebene Minutenzahl (1, 3 oder 5)."""
        if minutes in [1, 3, 5]:
            self.timer_duration = minutes * 60  # Umrechnung in Sekunden
            self.time_remaining = self.timer_duration
            return True
        return False
    
    def start_timer(self):
        """Startet den Timer."""
        if self.timer_duration > 0:
            self.timer_active = True
            return True
        return False
    
    def stop_timer(self):
        """Stoppt den Timer."""
        self.timer_active = False
    
    def reset_timer(self):
        """Setzt den Timer zurück."""
        self.time_remaining = self.timer_duration
        self.timer_active = False
    
    def update_timer(self):
        """
        Aktualisiert den Timer (zählt eine Sekunde herunter).
        Gibt True zurück, wenn der Timer noch läuft, False wenn er abgelaufen ist.
        """
        if not self.timer_active:
            return False
            
        if self.time_remaining > 0:
            self.time_remaining -= 1
            return True
        else:
            self.timer_active = False
            return False
    
    def get_time_remaining_str(self):
        """Gibt die verbleibende Zeit als formatierte Zeichenkette zurück (MM:SS)."""
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        return f"{minutes:02d}:{seconds:02d}"