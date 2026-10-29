# Blog-Code-Beispiele

Lauffähige Beispiele zu den Artikeln auf christian-blab.com. Jeder Ordner gehört zu einem Artikel und enthält den vollständigen Code, Beispieldaten, eine kurze Anleitung und Unit-Tests.

| Artikel | Ordner | Inhalt |
|---|---|---|
| [Obsidian: Ein Notizbuch, das auch deine KI lesen kann](https://christian-blab.com/obsidian-als-wissensbasis-fuer-ki-agenten) | — | kein Code |
| [Wie du einer KI nur die passenden Notizen gibst](https://christian-blab.com/warum-ki-agenten-einen-kontext-router-brauchen) | [`02-kontext-router/`](02-kontext-router/) | Notizen auswählen, Dateien nach Markdown umwandeln |
| [Das Gedächtnis deiner KI gehört in Dateien](https://christian-blab.com/agent-memory-engineering) | [`03-gedaechtnis/`](03-gedaechtnis/) | Notizen mit Datum, Ablauf und Prüfskript |
| [KI-Werkzeuge unter Windows einrichten: WSL](https://christian-blab.com/ki-agenten-windows-wsl-linux) | — | kein Code |
| [Einen KI-Assistenten im Terminal einrichten](https://christian-blab.com/opencode-mcp-tmux-entwicklungsumgebung) | — | kein Code |
| [Skills für KI: Anleitungen, die sie bei Bedarf selbst findet](https://christian-blab.com/skill-first-statt-prompt-first) | [`06-skill-first/`](06-skill-first/) | Skill-Katalog aus `SKILL.md`-Dateien bauen |

Die Links auf christian-blab.com gehen erst live, wenn der Blog die Artikel veröffentlicht hat. Bis dahin führen die Ordnerlinks im Repository zu den Beispielen.

## Voraussetzungen

- Python ab Version 3.10 (nur Standardbibliothek, außer MarkItDown in `02`)
- Windows: Python über `winget install Python.Python.3.12`, danach PowerShell neu öffnen
- Linux (Ubuntu, Debian): `sudo apt install python3`

## Aufruf unter Linux

```bash
python3 02-kontext-router/router.py 02-kontext-router/beispieldaten/Notizen "Bis wann kann ich die Haftpflicht kündigen?"
python3 03-gedaechtnis/verfall.py 03-gedaechtnis/beispiel-garten
python3 06-skill-first/skill_katalog.py 06-skill-first/beispiel-skills
```

## Aufruf unter Windows (PowerShell)

```powershell
py 02-kontext-router\router.py 02-kontext-router\beispieldaten\Notizen "Bis wann kann ich die Haftpflicht kündigen?"
py 03-gedaechtnis\verfall.py 03-gedaechtnis\beispiel-garten
py 06-skill-first\skill_katalog.py 06-skill-first\beispiel-skills
```

Jeder Ordner hat eine eigene `README.md` mit weiteren Beispielen, dem Aufruf für `umwandeln.py` und der Erklärung der Ausgabe.

## Tests

Linux:

```bash
python3 -m unittest discover -s 02-kontext-router/tests -v
python3 -m unittest discover -s 03-gedaechtnis/tests -v
python3 -m unittest discover -s 06-skill-first/tests -v
```

Windows (PowerShell):

```powershell
py -m unittest discover -s 02-kontext-router\tests -v
py -m unittest discover -s 03-gedaechtnis\tests -v
py -m unittest discover -s 06-skill-first\tests -v
```

Wenn `pytest` installiert ist, funktionieren auch folgende Befehle:

```bash
python3 -m pytest 02-kontext-router/tests 03-gedaechtnis/tests 06-skill-first/tests -q
```

## Lizenz

MIT, siehe [LICENSE](LICENSE). Inhaber: Christian Blab, 2026.

## Hinweis

Die Beispiele arbeiten mit erfundenen Daten. Lege keine Passwörter, Zugangsdaten oder persönlichen Dokumente in Beispielordner.
