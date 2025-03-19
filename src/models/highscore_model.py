import json
from datetime import datetime

class Highscore:
    def __init__(self, name, score, duration, words_per_minute, date=None):
        self.name = name
        self.score = score
        self.duration = duration  # in Minuten (1, 3 oder 5)
        self.words_per_minute = words_per_minute
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M")

class HighscoreModel:
    def __init__(self, file_path='highscores.json'):
        self.file_path = file_path
        self.highscores = []
        self.load_highscores()
        
    def add_highscore(self, name, score, duration, words_per_minute):
        """Fügt einen neuen Highscore hinzu"""
        highscore = Highscore(name, score, duration, words_per_minute)
        self.highscores.append(highscore)
        self.highscores.sort(key=lambda x: x.score, reverse=True)  # Sortieren nach Punktzahl
        self.save_highscores()
        return True
        
    def get_highscores(self, duration=None, limit=10):
        """Gibt die top X Highscores zurück, optional gefiltert nach Dauer"""
        if duration:
            filtered = [h for h in self.highscores if h.duration == duration]
            return filtered[:limit]
        return self.highscores[:limit]
        
    def save_highscores(self):
        """Speichert Highscores in JSON-Datei"""
        data = []
        for h in self.highscores:
            data.append({
                'name': h.name,
                'score': h.score,
                'duration': h.duration,
                'words_per_minute': h.words_per_minute,
                'date': h.date
            })
            
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    def load_highscores(self):
        """Lädt Highscores aus JSON-Datei"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.highscores = []
            for item in data:
                highscore = Highscore(
                    item['name'],
                    item['score'],
                    item['duration'],
                    item['words_per_minute'],
                    item['date']
                )
                self.highscores.append(highscore)
                
            # Nach Punktzahl sortieren
            self.highscores.sort(key=lambda x: x.score, reverse=True)
                
        except (FileNotFoundError, json.JSONDecodeError):
            # Erstelle leere Liste, wenn Datei nicht existiert oder fehlerhaft ist
            self.highscores = []