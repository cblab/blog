#!/usr/bin/env python3
"""Sucht in einem Ordner mit Notizen die passendsten heraus und baut daraus eine fertige Anfrage an die KI.

Aufruf:  python3 router.py ORDNER "Deine Frage" [Anzahl]
"""
import re
import sys
from pathlib import Path
from datetime import date

FUELLWOERTER = set("""der die das den dem des ein eine einen einem einer und oder aber ich du wir ihr sie
ist sind war waren hat haben wird werden kann kannst können muss müssen soll sollen mit von für auf aus bei nach
vor über unter zum zur zur wie was wer wann wo warum welche welcher welches nicht noch schon auch mein meine
meinen meinem meiner dein deine sich als wenn dass ob nur sehr mehr""".split())

def stamm(wort):
    return wort[:5]

def woerter(text):
    return re.findall(r"[a-zäöüß0-9]{3,}", text.lower())

def kopf(pfad):
    zeilen = pfad.read_text(encoding="utf-8").lstrip("\ufeff").splitlines()
    werte = {}
    yaml_kopf = bool(zeilen and zeilen[0].strip() == "---")
    for zeile in zeilen[1:] if yaml_kopf else zeilen:
        if (yaml_kopf and zeile.strip() == "---") or (not yaml_kopf and not zeile.strip()):
            break
        treffer = re.match(r"^([A-Za-zäöüÄÖÜ ]+):\s*(.*)$", zeile)
        if treffer:
            werte[treffer.group(1).strip().lower()] = treffer.group(2).strip()
    return werte

def lies_notiz(pfad):
    return pfad.read_text(encoding="utf-8"), kopf(pfad)

def bewerte(frage_woerter, text, kopf):
    kopftext = kopf.get("titel", "") + " " + kopf.get("thema", "") + " " + kopf.get("kurz", "")
    kopf_staemme = {stamm(w) for w in woerter(kopftext)}
    text_staemme = [stamm(w) for w in woerter(text)]
    punkte = 0
    for w in frage_woerter:
        s = stamm(w)
        if s in kopf_staemme:
            punkte += 3
        punkte += min(text_staemme.count(s), 3)
    return punkte

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    ordner = Path(sys.argv[1]).expanduser()
    frage = sys.argv[2]
    try:
        anzahl = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    except ValueError:
        sys.exit("Anzahl muss eine positive ganze Zahl sein.")
    if not ordner.is_dir() or anzahl < 1:
        sys.exit("Ordner fehlt oder Anzahl ist nicht positiv.")
    frage_woerter = [w for w in woerter(frage) if w not in FUELLWOERTER]

    treffer = []
    for pfad in sorted(ordner.rglob("*.md")):
        text, kopf = lies_notiz(pfad)
        if kopf.get("status", "gilt").lower() not in ("gilt", "zu prüfen"):
            continue
        if kopf.get("gilt bis"):
            try:
                if date.fromisoformat(kopf["gilt bis"]) < date.today():
                    continue
            except ValueError:
                continue
        punkte = bewerte(frage_woerter, text, kopf)
        if punkte > 0:
            treffer.append((punkte, pfad, text))
    treffer.sort(key=lambda t: t[0], reverse=True)
    treffer = treffer[:anzahl]

    print("Beantworte die Frage nur mit den Notizen unten.")
    print("Nenne zu jeder Aussage den Dateinamen der Notiz und die konkrete Belegstelle.")
    print("Angaben mit Status zu prüfen bleiben unbestätigt; weise auf Widersprüche hin.")
    print("Steht die Antwort nicht in den Notizen, schreibe genau: nicht belegt.")
    print("Rate nicht und nutze kein Wissen von außerhalb.\n")
    print("FRAGE: " + frage + "\n")
    if not treffer:
        print("(Es wurde keine passende Notiz gefunden. Antworte: nicht belegt.)")
    for punkte, pfad, text in treffer:
        print("--- Notiz: %s (Treffer: %d) ---" % (pfad.relative_to(ordner).as_posix(), punkte))
        print(text.strip() + "\n")

if __name__ == "__main__":
    main()
