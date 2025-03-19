class StatisticsModel:
    def __init__(self, model):
        self.main_model = model
        # Tracking für alle Tastenanschläge während des gesamten Tests
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.case_error_keystrokes = 0
        self.wrong_keystrokes = 0
        self.backspaces = 0
        self.max_keystrokes_per_second = 0.0  # Maximale Tippgeschwindigkeit
        
    def track_keystroke(self, key_char, target_char=None, is_backspace=False):
        """Verfolgt jeden einzelnen Tastenanschlag und klassifiziert ihn"""
        if is_backspace:
            self.backspaces += 1
            return
        
        self.total_keystrokes += 1
        
        if target_char is None:
            return  # Kein Vergleichszeichen verfügbar
            
        if key_char == target_char:
            self.correct_keystrokes += 1
        elif key_char.lower() == target_char.lower():
            self.case_error_keystrokes += 1
        else:
            self.wrong_keystrokes += 1
    
    def calculate_typing_statistics(self, typed_text):
        """
        Berechnet die Tippstatistik basierend auf dem Status der eingegebenen Zeichen.
        """
        # Status-Liste aus dem Hauptmodell abrufen (endgültiger Zustand)
        status_list = self.main_model.check_typing(typed_text)
        
        # 1. Zeichenstatistik - endgültiger Status
        char_correct = status_list.count(1)  # Grün (korrekt)
        char_case_error = status_list.count(2)  # Gelb (Groß-/Kleinschreibung)
        char_wrong = status_list.count(3)  # Rot (falsch)
        
        # Erweiterte Statistik mit allen erfassten Tastenanschlägen
        char_stats = {
            'correct': char_correct,
            'case_error': char_case_error,
            'wrong': char_wrong,
            'total_keystrokes': self.total_keystrokes,
            'total_correct': self.correct_keystrokes,
            'total_case_error': self.case_error_keystrokes, 
            'total_wrong': self.wrong_keystrokes,
            'backspaces': self.backspaces,
            'error_rate': self.calculate_error_rate()
        }
        
        # 2. Wortstatistik - bleibt unverändert
        target_words = self.main_model.current_text.split()
        typed_words = typed_text.split()
        
        word_correct = 0
        word_case_error = 0
        word_wrong = 0
        
        # Vergleiche jedes Wort
        for i, target_word in enumerate(target_words):
            if i >= len(typed_words):
                break  # Nicht genug getippte Wörter
                
            typed_word = typed_words[i]
            
            # Prüfe Wort auf Korrektheit
            if typed_word == target_word:
                word_correct += 1
            elif typed_word.lower() == target_word.lower():
                word_case_error += 1  # Nur Groß-/Kleinschreibung unterschiedlich
            else:
                # Prüfe, ob das Wort Tippfehler enthält (rot)
                has_wrong_char = False
                for j in range(min(len(typed_word), len(target_word))):
                    char_index = sum(len(w) + 1 for w in target_words[:i]) + j
                    if char_index < len(status_list) and status_list[char_index] == 3:
                        has_wrong_char = True
                        break
                
                if has_wrong_char:
                    word_wrong += 1
                else:
                    word_case_error += 1  # Nur Groß-/Kleinschreibung oder Längenunterschied
        
        stats = {
            'char': char_stats,
            'word': {
                'correct': word_correct,
                'case_error': word_case_error,
                'wrong': word_wrong
            }
        }
        
        return stats
        
    def calculate_error_rate(self):
        """Berechnet die Fehlerrate (Prozent der Fehler an allen Tastenanschlägen)"""
        if self.total_keystrokes == 0:
            return 0.0
        
        total_errors = self.case_error_keystrokes + self.wrong_keystrokes
        error_rate = (total_errors / self.total_keystrokes) * 100
        return round(error_rate, 1)
    
    def update_max_speed(self, current_speed):
        """Aktualisiert die maximale Tippgeschwindigkeit"""
        if current_speed > self.max_keystrokes_per_second:
            self.max_keystrokes_per_second = current_speed