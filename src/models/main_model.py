import os
import random

class MainModel:
    def __init__(self):        
        self.keystroke_count = 0  # Zählt die Tastenanschläge
        self.elapsed_time = 0     # Verstrichene Zeit in Sekunden seit Beginn der Eingabe
        
        # Timer-Attribute
        self.timer_duration = 0  # Dauer in Sekunden (0, 60, 180, 300)
        self.time_remaining = 0  # Verbleibende Zeit in Sekunden
        self.timer_active = False  # Gibt an, ob der Timer aktiv ist
        
        # Wortliste-Attribute
        self.all_words = []       # Alle verfügbaren Wörter
        self.used_words = []      # Bereits verwendete Wörter
        self.current_text = ""    # Aktueller zu tippender Text
        self.typed_correctly = 0  # Anzahl korrekt getippter Zeichen
        self.max_words = 1000     # Maximale Anzahl zu verwendender Wörter
        self.words_count = 0      # Zähler für bereits verwendete Wörter
        
        # Wortliste laden
        self.load_word_list()
    
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
            # Zeit aktualisieren
            self.elapsed_time = self.timer_duration - self.time_remaining
            return True
        else:
            self.timer_active = False
            return False
    
    def get_keystrokes_per_second(self):
        """Berechnet die Anschläge pro Sekunde."""
        if self.timer_active and self.elapsed_time > 0:
            # Verwende die verstrichene Zeit, ohne die Variable zu überschreiben
            elapsed = self.elapsed_time  # Neue temporäre Variable
            # Anschläge durch verstrichene Zeit
            return round(self.keystroke_count / elapsed, 1)
        return 0.0
    
    def get_time_remaining_str(self):
        """Gibt die verbleibende Zeit als formatierte Zeichenkette zurück (MM:SS)."""
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def load_word_list(self, file_path=None):
        """Lädt die Wortliste aus einer Datei."""
        if file_path is None:
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                    'ressources', 'wortschatzGrund1.txt')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Wörter laden und leere Zeilen sowie Kommentare filtern
                self.all_words = [word.strip() for word in file.readlines() 
                                 if word.strip() and not word.strip().startswith('//')]
            
            # Wortliste mischen
            random.shuffle(self.all_words)
            
        except Exception as e:
            print(f"Fehler beim Laden der Wortliste: {e}")
            # Fallback: Leere Liste
            self.all_words = []
    
    def get_next_words(self, count=20):
        """Gibt die nächsten 'count' Wörter zurück."""
        if not self.all_words and not self.used_words:
            return []  # Keine Wörter verfügbar
            
        words_needed = count
        result = []
        
        # Wenn nicht genug Wörter in all_words, used_words wiederverwenden
        if len(self.all_words) < words_needed:
            # Used words wiederverwenden, wenn alle Wörter verbraucht sind
            self.all_words.extend(self.used_words)
            self.used_words = []
            random.shuffle(self.all_words)
        
        # Wörter aus all_words nehmen und zu used_words hinzufügen
        for _ in range(min(words_needed, len(self.all_words))):
            if self.words_count >= self.max_words:
                break  # Maximale Wortanzahl erreicht
                
            word = self.all_words.pop(0)
            result.append(word)
            self.used_words.append(word)
            self.words_count += 1
            
        return result
    
    def generate_text_for_typing(self, words_count=20):
        """Generiert einen Text zum Abtippen."""
        words = self.get_next_words(words_count)
        if not words:
            return ""
            
        # Text mit Leerzeichen zwischen den Wörtern generieren
        self.current_text = " ".join(words)
        self.typed_correctly = 0  # Reset der korrekten Zeichen
        return self.current_text
    
    def check_typing(self, typed_text):
        """
        Überprüft den eingegebenen Text und gibt eine Liste mit Status-Codes zurück:
        0 = noch nicht getippt
        1 = korrekt getippt (grün)
        2 = falsche Groß-/Kleinschreibung oder ähnliche Buchstaben (gelb)
        3 = falscher Buchstabe (rot)
        """
        result = [0] * len(self.current_text)  # Alle Zeichen als "noch nicht getippt" markieren
        correct_count = 0
        
        for i, target_char in enumerate(self.current_text):
            if i >= len(typed_text):
                break  # Ende des getippten Textes erreicht
            
            typed_char = typed_text[i]
            
            if target_char == typed_char:
                # Exakt gleicher Buchstabe (gleiche Groß-/Kleinschreibung)
                result[i] = 1
                correct_count += 1
            elif target_char.lower() == typed_char.lower():
                # Gleicher Buchstabe, aber unterschiedliche Groß-/Kleinschreibung
                result[i] = 2
            elif self.are_similar_chars(target_char, typed_char):
                # Ähnliche Buchstaben (z.B. Umlaut und Basis-Buchstabe)
                result[i] = 2
            else:
                # Komplett falscher Buchstabe
                result[i] = 3
        
        self.typed_correctly = correct_count
        return result

    def are_similar_chars(self, char1, char2):
        """
        Prüft, ob zwei Zeichen als ähnlich gelten (Umlaute und ihre Basis-Buchstaben)
        """
        # Beide Zeichen in Kleinbuchstaben umwandeln
        char1 = char1.lower()
        char2 = char2.lower()
        
        # Bekannte Paare von ähnlichen Buchstaben
        similar_pairs = [
            {'ä', 'a'},
            {'ö', 'o'},
            {'ü', 'u'},
            {'ß', 'ss', 's'}
        ]
        
        # Prüfen, ob die beiden Zeichen im gleichen Set sind
        for pair in similar_pairs:
            if char1 in pair and char2 in pair:
                return True
                
        return False