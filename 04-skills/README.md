# Teil 4 – Skills verwenden

Dieser Ordner gehört zu Teil 4 der Serie.

`skill_katalog.py` liest `SKILL.md` aus direkt untergeordneten Skill-Ordnern und schreibt `KATALOG.md` (eine Zeile pro Skill). Keine Modellaufrufe, keine Installation, keine automatische Auswahl. `name` und `description` müssen nicht leer und einzeilig im YAML-Kopf stehen. Kein vollständiger YAML-Parser.

Alle Befehle aus dem Hauptordner ausführen.

Linux:

```bash
python3 04-skills/skill_katalog.py 04-skills/beispiel-skills
```

Windows PowerShell:

```powershell
py 04-skills\skill_katalog.py 04-skills\beispiel-skills
```

Der Katalog liegt anschließend in `04-skills/beispiel-skills/KATALOG.md`.

| Aufgabe | Erwarteter Skill |
|---|---|
| Anfrage an eine Transporterfirma entwerfen | brief-schreiben |
| Tabellensummen prüfen | tabelle-pruefen |
| Sitzungsprotokoll schreiben | keiner |
| Transportbeschluss aus einer Notiz nachlesen | keiner |

Zuerst nur Katalog und Aufgabe zur Auswahl übergeben. Danach den Inhalt der passenden Anleitung und die Faktennotizen laden. Keine Anleitung erzwingen, wenn sie nicht passt. Ein Skill enthält Anweisungen, keine Faktenbestätigung und keine technischen Berechtigungen. Das Kopieren in einen beliebigen Ordner bewirkt keine automatische Erkennung in jedem Assistenten.

## Tests

```bash
python3 -m unittest discover -s 04-skills/tests -v
```

Unter Windows `py` und Backslashes. Nur Standardbibliothek.

[Zur Serienübersicht](../README.md) · [Voriger Teil](../03-gedaechtnis/README.md) · [Nächster Teil](../05-terminal/README.md)
