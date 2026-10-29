#!/usr/bin/env python3
"""Sucht in einem Ordner mit Notizen die passendsten heraus und baut daraus eine fertige Anfrage an die KI.

Aufruf:  python3 router.py ORDNER "Deine Frage" [Anzahl]
"""
import re
import sys
from pathlib import Path

FUELLWOERTER = set("""der die das den dem des ein eine einen einem einer und oder aber ich du wir ihr sie
ist sind war waren hat haben wird werden kann kannst können muss müssen soll sollen mit von für auf aus bei nach
vor über unter zum zur zur wie was wer wann wo warum welche welcher welches nicht noch schon auch mein meine
meinen meinem meiner dein deine sich als wenn dass ob nur sehr mehr""".split())

def stamm(wort):
    return wort[:5]

def woerter(text):
    return re.findall(r"[a-zäöüß0-9]{3,}", text.lower())

def lies_notiz(pfad):
    text = pfad.read_text(encoding="utf-8")
    kopf = {}
    zeilen = text.splitlines()
    for zeile in zeilen[:8]:
        if ":" in zeile:
            schluessel, wert = zeile.split(":", 1)
            kopf[schluessel.strip().lower()] = wert.strip()
    return text, kopf

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
    anzahl = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    frage_woerter = [w for w in woerter(frage) if w not in FUELLWOERTER]

    treffer = []
    for pfad in sorted(ordner.rglob("*.md")):
        text, kopf = lies_notiz(pfad)
        if kopf.get("status", "gilt").lower() == "veraltet":
            continue
        punkte = bewerte(frage_woerter, text, kopf)
        if punkte > 0:
            treffer.append((punkte, pfad, text))
    treffer.sort(key=lambda t: t[0], reverse=True)
    treffer = treffer[:anzahl]

    print("Beantworte die Frage nur mit den Notizen unten.")
    print("Nenne zu jeder Aussage den Dateinamen der Notiz.")
    print("Steht die Antwort nicht in den Notizen, schreibe genau: nicht belegt.")
    print("Rate nicht und nutze kein Wissen von außerhalb.\n")
    print("FRAGE: " + frage + "\n")
    if not treffer:
        print("(Es wurde keine passende Notiz gefunden. Antworte: nicht belegt.)")
    for punkte, pfad, text in treffer:
        print("--- Notiz: %s (Treffer: %d) ---" % (pfad.name, punkte))
        print(text.strip() + "\n")

if __name__ == "__main__":
    main()
