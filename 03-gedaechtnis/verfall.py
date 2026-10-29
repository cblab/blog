#!/usr/bin/env python3
"""Zeigt Notizen, die du prüfen solltest: abgelaufen, ohne Datum oder lange nicht angefasst.

Aufruf:  python3 verfall.py ORDNER [Tage]
Jede Notiz beginnt mit Kopfzeilen wie  "Stand: 2026-03-01"  und optional  "Gilt bis: 2026-09-30".
"""
import re
import sys
from datetime import date, datetime
from pathlib import Path

def datum(text):
    try:
        return datetime.strptime(text.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None

def kopf(pfad):
    werte = {}
    for zeile in pfad.read_text(encoding="utf-8").splitlines()[:8]:
        treffer = re.match(r"^([A-Za-zäöüÄÖÜ ]+):\s*(.*)$", zeile)
        if treffer:
            werte[treffer.group(1).strip().lower()] = treffer.group(2).strip()
    return werte

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ordner = Path(sys.argv[1]).expanduser()
    grenze = int(sys.argv[2]) if len(sys.argv) > 2 else 180
    heute = date.today()
    meldungen = []
    for pfad in sorted(ordner.rglob("*.md")):
        werte = kopf(pfad)
        if werte.get("status", "gilt").lower() == "veraltet":
            continue
        ablauf = datum(werte.get("gilt bis", ""))
        stand = datum(werte.get("stand", ""))
        if ablauf and ablauf < heute:
            meldungen.append((pfad.name, "abgelaufen am %s: auf 'veraltet' setzen oder erneuern" % ablauf))
        elif stand is None:
            meldungen.append((pfad.name, "kein gültiges Datum bei 'Stand:'"))
        elif (heute - stand).days > grenze:
            meldungen.append((pfad.name, "Stand vor %d Tagen: noch aktuell?" % (heute - stand).days))
    if not meldungen:
        print("Alles in Ordnung.")
    for name, text in meldungen:
        print("%-30s %s" % (name, text))

if __name__ == "__main__":
    main()
