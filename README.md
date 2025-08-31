Interactive movie search: Interaktive Filmsuche

Beschreibung:
Dies ist eine interaktive Konsolenanwendung in Python, mit der Filme aus einer MySQL-Datenbank gesucht und analysiert werden können. Alle Suchanfragen werden in MongoDB gespeichert, und die Anwendung zeigt eine Statistik der beliebtesten Suchanfragen.

Funktionen:
- Filmsuche
- Nach Schlüsselwort oder Titel (mit Paginierung: jeweils 10 Ergebnisse)
- Nach Genre und Veröffentlichungsjahr (Angabe von Unter- und Obergrenze oder einem konkreten Jahr)
- Detaillierte Filmansicht
- Möglichkeit, vollständige Informationen zu einem ausgewählten Film aus der Ergebnisliste anzuzeigen
- Speicherung von Suchanfragen
- Alle Suchanfragen werden in einer MongoDB-Collection protokolliert
- Statistik
- Anzeige der 5 beliebtesten Suchanfragen nach Häufigkeit und den letzten Suchen

Technologien:
- Python
- MySQL (Filmdaten)
- MongoDB (Protokollierung von Suchanfragen)

Bibliotheken: pymysql, pymongo u.a.

Installation:
- Repository klonen
  git clone https://github.com/AleX5andr/ich_python-db.git
- Abhängigkeiten installieren
  pip install -r requirements.txt
- Datenbanken vorbereiten
  MySQL: Filme-Datenbank einrichten
  MongoDB: Collection für Suchanfragen erstellen

Nutzung:
  Anwendung starten - python main.py

Den Anweisungen im Konsolenmenü folgen, um Filme zu suchen, Details anzusehen oder die Statistik zu prüfen.

Beitragende
Projekt von Oleksandr Muntian

Lizenz - Dieses Projekt ist unter der MIT-Lizenz lizenziert.
