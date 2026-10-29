# 03 — Gedächtnis in Dateien

Beispiel zum Artikel „Das Gedächtnis deiner KI gehört in Dateien, nicht in den Chat".

## Inhalt

- `verfall.py` — meldet Notizen mit abgelaufenem `Gilt bis`, fehlendem `Stand`
  oder altem Stand
- `vorlagen/` — drei leere Startdateien (`Über-mich.md`, `Regeln.md`,
  `Entscheidungen.md`)
- `beispiel-garten/` — ausgefüllter Beispielordner
- `tests/` — Unit-Tests

## Aufruf unter Linux

```bash
python3 verfall.py beispiel-garten
python3 verfall.py beispiel-garten 90
```

## Aufruf unter Windows (PowerShell)

```powershell
py verfall.py beispiel-garten
py verfall.py beispiel-garten 90
```

Die zweite Zahl ist die Frist in Tagen; ohne Angabe gelten 180 Tage.

## Tests

Linux:

```bash
python3 -m unittest discover -s 03-gedaechtnis/tests -v
```

Windows:

```powershell
py -m unittest discover -s 03-gedaechtnis\tests -v
```
