"""Tests für umwandeln.py mit einem Ersatz für MarkItDown, damit nichts installiert sein muss.
Start: python3 -m unittest discover -s 02-kontext-router/tests -v"""
import contextlib
import importlib
import io
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

HIER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HIER))

class Ergebnis:
    def __init__(self, text):
        self.text_content = text

class FalscherUmwandler:
    """Ersatz für markitdown.MarkItDown: liefert den Dateiinhalt, bei 'kaputt' einen Fehler."""
    def convert(self, pfad):
        if "kaputt" in pfad:
            raise ValueError("Datei nicht lesbar")
        return Ergebnis("# Umgewandelt\n\n" + Path(pfad).read_text(encoding="utf-8"))

def lade_modul():
    falsches = types.ModuleType("markitdown")
    falsches.MarkItDown = FalscherUmwandler
    with mock.patch.dict(sys.modules, {"markitdown": falsches}):
        sys.modules.pop("umwandeln", None)
        return importlib.import_module("umwandeln")

class UmwandelnTest(unittest.TestCase):
    def setUp(self):
        self.modul = lade_modul()
        self.tmp = tempfile.TemporaryDirectory()
        self.quelle = Path(self.tmp.name) / "Unterlagen"
        self.ziel = Path(self.tmp.name) / "Notizen"
        (self.quelle / "Versicherung").mkdir(parents=True)
        (self.quelle / "Versicherung" / "haftpflicht.txt").write_text("Vertrag 62 Euro", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def starte(self):
        alt = sys.argv
        sys.argv = ["umwandeln.py", str(self.quelle), str(self.ziel)]
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                self.modul.main()
        finally:
            sys.argv = alt

    def test_unterordner_bleiben_erhalten(self):
        self.starte()
        self.assertTrue((self.ziel / "Versicherung" / "haftpflicht.md").exists())

    def test_notizkopf_enthaelt_thema_status_und_quelle(self):
        self.starte()
        text = (self.ziel / "Versicherung" / "haftpflicht.md").read_text(encoding="utf-8")
        self.assertIn("Thema: Versicherung", text)
        self.assertIn("Status: zu prüfen", text)
        self.assertIn("Importiert am:", text)
        self.assertIn("Quelle: Versicherung/haftpflicht.txt", text)
        self.assertIn("Stand: ", text)
        self.assertIn("Vertrag 62 Euro", text)

    def test_zweiter_lauf_ueberspringt_vorhandene(self):
        self.starte()
        vorher = (self.ziel / "Versicherung" / "haftpflicht.md").stat().st_mtime_ns
        self.starte()
        nachher = (self.ziel / "Versicherung" / "haftpflicht.md").stat().st_mtime_ns
        self.assertEqual(vorher, nachher)

    def test_fehlerhafte_datei_stoppt_nicht_den_rest(self):
        (self.quelle / "Versicherung" / "kaputt.txt").write_text("x", encoding="utf-8")
        self.starte()
        self.assertTrue((self.ziel / "Versicherung" / "haftpflicht.md").exists())
        self.assertFalse((self.ziel / "Versicherung" / "kaputt.md").exists())

    def test_unbekannte_endungen_werden_ignoriert(self):
        (self.quelle / "Versicherung" / "bild.xyz").write_text("x", encoding="utf-8")
        self.starte()
        self.assertFalse((self.ziel / "Versicherung" / "bild.md").exists())

    def test_originale_bleiben_unveraendert(self):
        self.starte()
        original = self.quelle / "Versicherung" / "haftpflicht.txt"
        self.assertEqual(original.read_text(encoding="utf-8"), "Vertrag 62 Euro")

if __name__ == "__main__":
    unittest.main()
