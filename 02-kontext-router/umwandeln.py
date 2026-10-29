#!/usr/bin/env python3
"""Wandelt alle Dateien eines Ordners (PDF, Word, Excel, PowerPoint, HTML ...) in Markdown-Notizen um.

Aufruf:  python3 umwandeln.py QUELLORDNER ZIELORDNER

Die Unterordner der Quelle bleiben erhalten und werden als "Thema" in den Notizkopf geschrieben.
Bereits umgewandelte Dateien werden übersprungen. Die Originale bleiben unverändert.
"""
import sys
from datetime import date, datetime
from pathlib import Path

from markitdown import MarkItDown

ENDUNGEN = {".pdf", ".docx", ".pptx", ".xlsx", ".html", ".htm", ".csv", ".json", ".xml", ".epub", ".txt"}

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    quelle = Path(sys.argv[1]).expanduser()
    ziel = Path(sys.argv[2]).expanduser()
    if not quelle.is_dir():
        sys.exit("Quellordner existiert nicht.")
    if ziel.resolve() == quelle.resolve() or quelle.resolve() in ziel.resolve().parents:
        sys.exit("Ziel muss außerhalb des Quellordners liegen.")
    umwandler = MarkItDown()
    ok, uebersprungen, fehler = 0, 0, []
    for datei in sorted(quelle.rglob("*")):
        if not datei.is_file() or datei.suffix.lower() not in ENDUNGEN:
            continue
        relativ = datei.relative_to(quelle)
        notiz = (ziel / relativ).with_suffix(".md")
        if notiz.exists():
            uebersprungen += 1
            continue
        try:
            text = umwandler.convert(str(datei)).text_content
        except Exception as fehlermeldung:
            fehler.append((relativ, str(fehlermeldung)[:80]))
            continue
        thema = relativ.parent.name or "Allgemein"
        stand = datetime.fromtimestamp(datei.stat().st_mtime).date().isoformat()
        kopf = "---\nTitel: %s\nThema: %s\nStatus: zu prüfen\nStand: \nKurz: \nQuelle: %s\nImportiert am: %s\nQuelldatei geändert am: %s\n---\n\n" % (datei.stem, thema, relativ.as_posix(), date.today().isoformat(), stand)
        notiz.parent.mkdir(parents=True, exist_ok=True)
        notiz.write_text(kopf + text.strip() + "\n", encoding="utf-8")
        ok += 1
    print("%d umgewandelt, %d übersprungen, %d Fehler." % (ok, uebersprungen, len(fehler)))
    for name, grund in fehler:
        print("Fehler bei %s: %s" % (name, grund))

if __name__ == "__main__":
    main()
