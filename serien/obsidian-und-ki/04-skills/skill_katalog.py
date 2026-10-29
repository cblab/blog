#!/usr/bin/env python3
"""Baut aus Skill-Ordnern eine Katalogdatei mit einer Zeile pro Skill.

Aufruf:  python3 skill_katalog.py SKILLS_ORDNER
Jeder Skill liegt in einem eigenen Ordner mit einer Datei SKILL.md. Diese beginnt so:

---
name: brief-schreiben
description: Schreibt kurze, freundliche Briefe und Mails ohne Floskeln.
---
"""
import re
import sys
from pathlib import Path

def lies_kopf(pfad):
    text = pfad.read_text(encoding="utf-8")
    treffer = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    werte = {}
    if treffer:
        for zeile in treffer.group(1).splitlines():
            if ":" in zeile:
                schluessel, wert = zeile.split(":", 1)
                werte[schluessel.strip()] = wert.strip()
    return werte

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ordner = Path(sys.argv[1]).expanduser()
    if not ordner.is_dir():
        sys.exit("Skills-Ordner fehlt.")
    zeilen, fehler = [], []
    for datei in sorted(ordner.glob("*/SKILL.md")):
        werte = lies_kopf(datei)
        if werte.get("name", "").strip() and werte.get("description", "").strip():
            zeilen.append("- %s: %s" % (werte["name"], werte["description"]))
        else:
            fehler.append(str(datei))
    katalog = ordner / "KATALOG.md"
    katalog.write_text("# Skill-Katalog\n\n" + "\n".join(zeilen) + "\n", encoding="utf-8")
    print("%d Skills in %s geschrieben." % (len(zeilen), katalog))
    for f in fehler:
        print("Kopf fehlt oder unvollständig:", f)

if __name__ == "__main__":
    main()
