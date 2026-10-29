"""Tests für router.py. Start: python3 -m unittest discover -s 02-kontext-router/tests -v"""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

HIER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HIER))
import router  # noqa: E402

DATEN = HIER / "tests" / "fixtures" / "notizen"

def lauf(ordner, frage, anzahl=None):
    argumente = ["router.py", str(ordner), frage] + ([str(anzahl)] if anzahl else [])
    alt = sys.argv
    sys.argv = argumente
    ausgabe = io.StringIO()
    try:
        with contextlib.redirect_stdout(ausgabe):
            router.main()
    finally:
        sys.argv = alt
    return ausgabe.getvalue()

class HilfsfunktionenTest(unittest.TestCase):
    def test_stamm_kuerzt_auf_fuenf_zeichen(self):
        self.assertEqual(router.stamm("kündigen"), "kündi")
        self.assertEqual(router.stamm("kündigungsfrist"), "kündi")

    def test_woerter_zerlegt_und_kleingeschrieben(self):
        self.assertEqual(router.woerter("Die Haftpflicht, 2026!"), ["die", "haftpflicht", "2026"])

    def test_woerter_ignoriert_sehr_kurze_woerter(self):
        self.assertEqual(router.woerter("ab im Ei"), [])

    def test_lies_notiz_liest_kopfzeilen(self):
        text, kopf = router.lies_notiz(DATEN / "Versicherung" / "haftpflicht.md")
        self.assertEqual(kopf["status"], "gilt")
        self.assertEqual(kopf["thema"], "Versicherung")
        self.assertIn("Nordlicht", text)

    def test_bewerte_gewichtet_kopf_hoeher_als_text(self):
        kopf = {"titel": "Haftpflicht", "thema": "", "kurz": ""}
        im_kopf = router.bewerte(["haftpflicht"], "Text ohne das Wort", kopf)
        nur_im_text = router.bewerte(["haftpflicht"], "Haftpflicht steht im Text", {})
        self.assertGreater(im_kopf, nur_im_text)

    def test_bewerte_ohne_treffer_ist_null(self):
        self.assertEqual(router.bewerte(["kontostand"], "Nur Garantie", {"titel": "Garantie"}), 0)

class AuswahlTest(unittest.TestCase):
    def test_findet_die_richtige_notiz(self):
        ausgabe = lauf(DATEN, "Wann kann ich die Haftpflicht kündigen?", 1)
        self.assertIn("haftpflicht.md", ausgabe)
        self.assertNotIn("waschmaschine.md", ausgabe)

    def test_veraltete_notiz_wird_uebersprungen(self):
        ausgabe = lauf(DATEN, "Haftpflicht Kündigungsfrist", 5)
        self.assertNotIn("haftpflicht-alt.md", ausgabe)

    def test_andere_frage_andere_notiz(self):
        ausgabe = lauf(DATEN, "Gilt die Garantie der Waschmaschine noch?", 1)
        self.assertIn("waschmaschine.md", ausgabe)

    def test_anzahl_begrenzt_die_treffer(self):
        ausgabe = lauf(DATEN, "Kündigungsfrist Versicherung", 1)
        self.assertEqual(ausgabe.count("--- Notiz:"), 1)

    def test_ohne_treffer_steht_nicht_belegt_in_der_anweisung(self):
        ausgabe = lauf(DATEN, "Wie hoch ist mein Kontostand?")
        self.assertIn("nicht belegt", ausgabe)
        self.assertNotIn("--- Notiz:", ausgabe)

    def test_anweisung_enthaelt_belegpflicht_und_frage(self):
        ausgabe = lauf(DATEN, "Wann kann ich die Haftpflicht kündigen?")
        self.assertIn("Nenne zu jeder Aussage den Dateinamen", ausgabe)
        self.assertIn("FRAGE: Wann kann ich die Haftpflicht kündigen?", ausgabe)

    def test_leerer_ordner_liefert_nicht_belegt(self):
        with tempfile.TemporaryDirectory() as leer:
            ausgabe = lauf(leer, "Irgendeine Frage zur Haftpflicht")
        self.assertIn("keine passende Notiz", ausgabe)

    def test_unterordner_werden_durchsucht(self):
        with tempfile.TemporaryDirectory() as t:
            tief = Path(t) / "a" / "b"
            tief.mkdir(parents=True)
            (tief / "x.md").write_text("Titel: Kürbissuppe\nStatus: gilt\n\nRezept mit Kürbis", encoding="utf-8")
            ausgabe = lauf(t, "Wie koche ich Kürbissuppe?")
        self.assertIn("x.md", ausgabe)

class SerienVertragTest(unittest.TestCase):
    def test_yaml_kopf_und_abgelaufene_notiz(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "alt.md").write_text("---\nTitel: Transport\nStatus: gilt\nGilt bis: 2000-01-01\n---\nTransport gebucht")
            (root / "offen.md").write_text("---\nTitel: Transport\nStatus: zu prüfen\n---\nTransport noch offen")
            output = lauf(root, "Transport")
            self.assertNotIn("--- Notiz: alt.md", output)
            self.assertIn("offen.md", output)
            self.assertIn("unbestätigt", output)

    def test_fliesstext_aendert_keinen_kopfstatus(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "notiz.md"
            path.write_text("Titel: Transport\nStatus: gilt\n\nStatus: veraltet\nTransport")
            self.assertEqual(router.lies_notiz(path)[1]["status"], "gilt")

    def test_fehlender_ordner_wird_gemeldet(self):
        with self.assertRaises(SystemExit):
            lauf(Path("/nicht-vorhandenes-serienbeispiel"), "Transport")

if __name__ == "__main__":
    unittest.main()
