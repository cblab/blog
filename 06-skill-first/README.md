# 06 — Skills für KI: Katalog bauen

Beispiel zum Artikel „Skills für KI: Anleitungen, die sie bei Bedarf selbst findet".
Das Skript liest die Kopfzeilen aller `SKILL.md`-Dateien und schreibt daraus
`KATALOG.md`, eine Zeile pro Skill.

## Inhalt

- `skill_katalog.py` — baut den Katalog
- `beispiel-skills/` — zwei fertige Skills (`brief-schreiben`, `tabelle-pruefen`)
- `tests/` — Unit-Tests

## Aufruf unter Linux

```bash
python3 skill_katalog.py beispiel-skills
```

## Aufruf unter Windows (PowerShell)

```powershell
py skill_katalog.py beispiel-skills
```

Die Ausgabe nennt die Zahl der geschriebenen Skills. Der Katalog liegt danach in
`beispiel-skills/KATALOG.md`.

## Tests

Linux:

```bash
python3 -m unittest discover -s 06-skill-first/tests -v
```

Windows:

```powershell
py -m unittest discover -s 06-skill-first\tests -v
```

Die Tests brauchen nur die Python-Standardbibliothek.
