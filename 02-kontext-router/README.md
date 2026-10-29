# Teil 2 – passende Notizen auswählen

Alle Befehle aus dem Hauptordner dieses Pakets ausführen (nicht aus diesem Unterordner).

Linux:

```bash
python3 02-kontext-router/router.py beispiele/umzug "Was ist beim Transport entschieden und was ist offen?"
```

Windows PowerShell:

```powershell
py 02-kontext-router\router.py beispiele\umzug "Was ist beim Transport entschieden und was ist offen?"
```

Die Ausgabe ist eine Anfrage zum manuellen Übergeben an einen Chat. Keine Anbieteraufrufe. Optional letzte Zahl: Anzahl Kandidaten, Standard 3. Gesucht wird über die ersten fünf Zeichen von Wörtern, stärker gewichtet in Titel, Thema, Kurz. Links werden nicht verfolgt. Veraltete und abgelaufene Notizen werden übersprungen; zu prüfende Angaben bleiben unbestätigt.

## Optional: Dokumente importieren

Erst eine virtuelle Umgebung anlegen; keine Originaldateien überschreiben.

Linux:

```bash
python3 -m venv .venv-import
.venv-import/bin/python -m pip install 'markitdown[pdf,docx,pptx,xlsx]'
.venv-import/bin/python 02-kontext-router/umwandeln.py beispiele/unterlagen Notizen-Import
```

Windows PowerShell:

```powershell
py -m venv .venv-import
.\.venv-import\Scripts\python.exe -m pip install "markitdown[pdf,docx,pptx,xlsx]"
.\.venv-import\Scripts\python.exe 02-kontext-router\umwandeln.py beispiele\unterlagen Notizen-Import
```

Quellen im eigenen Ordner lassen. Importstatus `zu prüfen`, Stand leer. Importiert am und Quelldatei geändert am sind keine Prüfdatumsangaben. Bestehende Markdown-Ziele werden übersprungen; es ist kein Abgleich nach Änderungen. Gleicher Stamm bei verschiedenen Dateiformaten kann zum selben Ziel führen; dann wird die zweite Datei ebenfalls übersprungen. Tabellen und Scans selbst prüfen, OCR ist nicht automatisch garantiert. Die Quelle ist eine erfundene kurze Textdatei.

## Tests

```bash
python3 -m unittest discover -s 02-kontext-router/tests -v
```

Unter Windows `py` statt `python3` und Backslashes. Der Importtest verwendet einen Ersatz für MarkItDown, keine echte Konvertierung. Ältere Haushalts-/Versicherungsnotizen dienen unter `tests/fixtures/notizen` nur als Testdaten.

[Zur Serienübersicht](../README.md) · [Voriger Teil](../01-obsidian/README.md) · [Nächster Teil](../03-gedaechtnis/README.md)
