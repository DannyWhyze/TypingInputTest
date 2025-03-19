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

    def calculate_score(self, typed_text):
        """Berechnet die Gesamtpunktzahl basierend auf der Tippstatistik"""
        stats = self.calculate_typing_statistics(typed_text)
        
        # Basispunkte: NUR für korrekte Zeichen (grüne)
        base_points = stats['char']['correct']
        
        # Abzüge für Fehler
        deductions = 0
        
        # Abzug für falsche Wörter (-2 pro Wort)
        deductions += stats['word']['wrong'] * 2
        
        # Abzug für halb-richtige Wörter (-1 pro Wort) - DIES FEHLTE
        deductions += stats['word']['case_error'] * 1
        
        # Spezieller Abzug für Wörter mit gemischten Fehlern
        mixed_error_words = self.count_mixed_error_words(typed_text)
        deductions += mixed_error_words * 2
        
        # Abzug für Backspaces (-1 pro Backspace)
        deductions += self.backspaces
        
        # Bonus für erfolgreiche Korrekturen (+0.5 pro Korrektur)
        corrections_bonus = min(self.backspaces, stats['char']['correct']) * 0.5
        
        # NEUE BONUS-REGELN:
        
        # 1. Wort-Sequenzen: +50 Punkte für 10 fehlerfreie Wörter hintereinander
        sequence_bonus = self.calculate_word_sequence_bonus(typed_text)
        
        # 2. Geschwindigkeit: Bonus basierend auf Anschlägen pro Minute
        speed_bonus = self.calculate_speed_bonus()
        
        # 3. Konstanz: +200 Punkte bei gleichmäßigem Tipprhythmus
        consistency_bonus = self.calculate_consistency_bonus()
        
        # Gesamtpunktzahl berechnen (nicht unter 0 gehen)
        total_score = max(0, base_points - deductions + corrections_bonus + 
                         sequence_bonus + speed_bonus + consistency_bonus)
        
        # Schwierigkeitsmultiplikator je nach Testdauer
        difficulty_multiplier = self.get_difficulty_multiplier()
        
        # Finale Punktzahl mit Schwierigkeitsgrad multiplizieren und runden
        final_score = round(total_score * difficulty_multiplier)
        
        return final_score

    def count_mixed_error_words(self, typed_text):
        """Zählt Wörter mit gemischten Fehlertypen (gelb und rot)"""
        mixed_error_words = 0
        
        # Text in Wörter aufteilen
        target_words = self.main_model.current_text.split()
        typed_words = typed_text.split()
        status_list = self.main_model.check_typing(typed_text)
        
        # Für jedes Wort prüfen wir, ob es gemischte Fehler hat
        start_idx = 0
        for i, target_word in enumerate(target_words):
            if i >= len(typed_words):
                break
                
            # Indizes für dieses Wort berechnen
            word_length = len(target_word)
            end_idx = start_idx + word_length
            
            # Status-Codes für dieses Wort extrahieren
            if end_idx <= len(status_list):
                word_status = status_list[start_idx:end_idx]
                
                # Prüfen, ob das Wort gelbe UND rote Markierungen hat
                has_yellow = 2 in word_status
                has_red = 3 in word_status
                
                if has_yellow and has_red:
                    mixed_error_words += 1
                    
            # Für nächstes Wort vorbereiten (inkl. Leerzeichen)
            start_idx = end_idx + 1
        
        return mixed_error_words

    def calculate_word_sequence_bonus(self, typed_text):
        """Bonus für Sequenzen von 10 fehlerfreien Wörtern in Folge"""
        target_words = self.main_model.current_text.split()
        typed_words = typed_text.split()
        status_list = self.main_model.check_typing(typed_text)
        
        bonus = 0
        correct_sequence = 0
        start_idx = 0
        
        for i, target_word in enumerate(target_words):
            if i >= len(typed_words):
                break
                
            word_length = len(target_word)
            end_idx = start_idx + word_length
            
            if end_idx <= len(status_list):
                word_status = status_list[start_idx:end_idx]
                
                if all(status == 1 for status in word_status):  # Alle Zeichen sind korrekt (grün)
                    correct_sequence += 1
                    if correct_sequence >= 10:
                        bonus += 50
                        correct_sequence = 0  # Zähler zurücksetzen nach Bonusvergabe
                else:
                    correct_sequence = 0  # Sequenz unterbrochen
                
            start_idx = end_idx + 1
        
        return bonus

    def calculate_speed_bonus(self):
        """Bonus basierend auf Anschlägen pro Minute"""
        keystrokes_per_minute = 0
        
        # Wenn genug Zeit vergangen ist, um Geschwindigkeit zu messen
        if self.main_model.elapsed_time > 0:
            # Anschläge pro Minute berechnen
            seconds = self.main_model.elapsed_time
            keystrokes_per_minute = (self.main_model.keystroke_count / seconds) * 60
        
        # Bonus basierend auf Geschwindigkeit
        if keystrokes_per_minute >= 100:
            return 500
        elif keystrokes_per_minute >= 80:
            return 250
        elif keystrokes_per_minute >= 60:
            return 100
        
        return 0

    def calculate_consistency_bonus(self):
        """Bonus für gleichmäßiges Tippen ohne große Geschwindigkeitsschwankungen"""
        # Diese Berechnung erfordert das Tracken von Geschwindigkeiten über Zeit
        # Wir verwenden eine vereinfachte Implementierung basierend auf 
        # dem Verhältnis von max_speed zu Durchschnittsgeschwindigkeit
        
        avg_speed = self.main_model.get_keystrokes_per_second()
        
        if avg_speed == 0:
            return 0
        
        # Konsistenz: Wenn die maximale Geschwindigkeit nicht mehr als 25% über dem Durchschnitt liegt
        # und nie unter 80% des Durchschnitts fällt, geben wir den Bonus
        if self.max_keystrokes_per_second <= avg_speed * 1.25 and self.max_keystrokes_per_second >= avg_speed * 0.8:
            return 200
        
        return 0

    def get_difficulty_multiplier(self):
        """Gibt den Schwierigkeitsmultiplikator je nach Timer-Dauer zurück"""
        if self.main_model.timer_duration == 60:      # 1 Minute
            return 1.0
        elif self.main_model.timer_duration == 180:    # 3 Minuten
            return 1.1
        elif self.main_model.timer_duration == 300:    # 5 Minuten
            return 1.2
        return 1.0