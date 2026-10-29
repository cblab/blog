"""Tests für verfall.py. Start: python3 -m unittest discover -s 03-gedaechtnis/tests -v"""
import contextlib
import io
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

HIER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HIER))
import verfall  # noqa: E402

def notiz(ordner, name, **kopf):
    zeilen = ["%s: %s" % (k.replace("_", " "), v) for k, v in kopf.items()]
    (Path(ordner) / name).write_text("Titel: " + name + "\n" + "\n".join(zeilen) + "\n\nText\n", encoding="utf-8")

def lauf(ordner, tage=None):
    alt = sys.argv
    sys.argv = ["verfall.py", str(ordner)] + ([str(tage)] if tage else [])
    ausgabe = io.StringIO()
    try:
        with contextlib.redirect_stdout(ausgabe):
            verfall.main()
    finally:
        sys.argv = alt
    return ausgabe.getvalue()

class DatumTest(unittest.TestCase):
    def test_gueltiges_datum(self):
        self.assertEqual(verfall.datum("2026-03-01"), date(2026, 3, 1))

    def test_ungueltiges_datum_ist_none(self):
        self.assertIsNone(verfall.datum("1. März 2026"))
        self.assertIsNone(verfall.datum(""))

class KopfTest(unittest.TestCase):
    def test_liest_schluessel_kleingeschrieben(self):
        kopf = verfall.kopf(HIER / "beispiel-garten" / "tomaten-beet-alt.md")
        self.assertEqual(kopf["status"], "veraltet")
        self.assertEqual(kopf["gilt bis"], "2026-03-31")

class MeldungenTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)
        self.heute = date.today()

    def tearDown(self):
        self.tmp.cleanup()

    def test_aktuelle_notiz_wird_nicht_gemeldet(self):
        notiz(self.ordner, "ok.md", Stand=self.heute.isoformat())
        self.assertIn("Alles in Ordnung", lauf(self.ordner))

    def test_abgelaufene_notiz_wird_gemeldet(self):
        gestern = (self.heute - timedelta(days=1)).isoformat()
        notiz(self.ordner, "alt.md", Stand=self.heute.isoformat(), Gilt_bis=gestern)
        ausgabe = lauf(self.ordner)
        self.assertIn("alt.md", ausgabe)
        self.assertIn("abgelaufen", ausgabe)

    def test_heute_ablaufende_notiz_ist_noch_gueltig(self):
        notiz(self.ordner, "heute.md", Stand=self.heute.isoformat(), Gilt_bis=self.heute.isoformat())
        self.assertIn("Alles in Ordnung", lauf(self.ordner))

    def test_fehlendes_datum_wird_gemeldet(self):
        (self.ordner / "ohne.md").write_text("Titel: ohne\n\nText\n", encoding="utf-8")
        self.assertIn("kein gültiges Datum", lauf(self.ordner))

    def test_lange_nicht_angefasste_notiz_wird_gemeldet(self):
        alt = (self.heute - timedelta(days=200)).isoformat()
        notiz(self.ordner, "lange.md", Stand=alt)
        self.assertIn("Stand vor 200 Tagen", lauf(self.ordner))

    def test_frist_laesst_sich_aendern(self):
        alt = (self.heute - timedelta(days=200)).isoformat()
        notiz(self.ordner, "lange.md", Stand=alt)
        self.assertIn("Alles in Ordnung", lauf(self.ordner, tage=365))

    def test_veraltete_notizen_werden_uebersprungen(self):
        notiz(self.ordner, "weg.md", Stand="2020-01-01", Status="veraltet")
        self.assertIn("Alles in Ordnung", lauf(self.ordner))

    def test_beispielordner_meldet_nur_nicht_veraltetes(self):
        ausgabe = lauf(HIER / "beispiel-garten")
        self.assertNotIn("tomaten-beet-alt.md", ausgabe)

if __name__ == "__main__":
    unittest.main()
