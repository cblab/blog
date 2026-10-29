# 02 — Kontext-Router

Beispiele zum Artikel „Wie du einer KI nur die passenden Notizen gibst, damit sie
besser antwortet".

## Inhalt

- `router.py` — wählt aus einem Notizordner die passendsten Dateien und baut eine
  fertige Anfrage mit Belegpflicht
- `umwandeln.py` — wandelt PDF, Word und andere Formate mit MarkItDown in
  Markdown-Notizen um
- `beispieldaten/` — kleiner Notizordner zum Ausprobieren
- `tests/` — Unit-Tests; `umwandeln.py` wird dabei mit einem Ersatz für MarkItDown
  getestet, damit nichts installiert werden muss

## Aufruf unter Linux

```bash
python3 router.py beispieldaten/Notizen "Bis wann kann ich die Haftpflicht kündigen?"
```

Für `umwandeln.py` zuerst MarkItDown in einer virtuellen Umgebung installieren:

```bash
python3 -m venv ~/mdenv
~/mdenv/bin/pip install 'markitdown[pdf,docx,pptx,xlsx]'
~/mdenv/bin/python umwandeln.py beispieldaten/Unterlagen beispieldaten/Notizen-Neu
```

## Aufruf unter Windows (PowerShell)

```powershell
py router.py beispieldaten\Notizen "Bis wann kann ich die Haftpflicht kündigen?"
```

```powershell
py -m venv $HOME\mdenv
$HOME\mdenv\Scripts\pip install "markitdown[pdf,docx,pptx,xlsx]"
$HOME\mdenv\Scripts\python umwandeln.py beispieldaten\Unterlagen beispieldaten\Notizen-Neu
```

## Tests

Linux:

```bash
python3 -m unittest discover -s 02-kontext-router/tests -v
```

Windows:

```powershell
py -m unittest discover -s 02-kontext-router\tests -v
```
