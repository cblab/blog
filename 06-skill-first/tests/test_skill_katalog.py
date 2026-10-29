"""Tests für skill_katalog.py. Start: python3 -m unittest discover -s 06-skill-first/tests -v"""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

HIER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HIER))
import skill_katalog  # noqa: E402


def skill(ordner, name, kopf, text="Anleitung\n"):
    ziel = Path(ordner) / name
    ziel.mkdir(parents=True)
    (ziel / "SKILL.md").write_text(kopf + text, encoding="utf-8")


def lauf(ordner):
    alt = sys.argv
    sys.argv = ["skill_katalog.py", str(ordner)]
    ausgabe = io.StringIO()
    try:
        with contextlib.redirect_stdout(ausgabe):
            skill_katalog.main()
    finally:
        sys.argv = alt
    return ausgabe.getvalue()


class KopfTest(unittest.TestCase):
    def test_liest_name_und_beschreibung(self):
        werte = skill_katalog.lies_kopf(HIER / "beispiel-skills" / "brief-schreiben" / "SKILL.md")
        self.assertEqual(werte["name"], "brief-schreiben")
        self.assertIn("freundliche Briefe", werte["description"])

    def test_beschreibung_darf_doppelpunkt_enthalten(self):
        with tempfile.TemporaryDirectory() as t:
            pfad = Path(t) / "SKILL.md"
            pfad.write_text("---\nname: x\ndescription: Prüft: Summen und Zellen\n---\n", encoding="utf-8")
            self.assertEqual(skill_katalog.lies_kopf(pfad)["description"], "Prüft: Summen und Zellen")

    def test_fehlt_der_kopf_ist_das_ergebnis_leer(self):
        with tempfile.TemporaryDirectory() as t:
            pfad = Path(t) / "SKILL.md"
            pfad.write_text("# Ohne Kopf\n", encoding="utf-8")
            self.assertEqual(skill_katalog.lies_kopf(pfad), {})


class KatalogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_schreibt_eine_zeile_pro_skill(self):
        skill(self.ordner, "b", "---\nname: b\ndescription: Zweiter Skill\n---\n")
        skill(self.ordner, "a", "---\nname: a\ndescription: Erster Skill\n---\n")
        lauf(self.ordner)
        text = (self.ordner / "KATALOG.md").read_text(encoding="utf-8")
        self.assertIn("- a: Erster Skill", text)
        self.assertIn("- b: Zweiter Skill", text)

    def test_sortiert_nach_ordnername(self):
        skill(self.ordner, "z", "---\nname: z\ndescription: Zuletzt\n---\n")
        skill(self.ordner, "a", "---\nname: a\ndescription: Zuerst\n---\n")
        lauf(self.ordner)
        text = (self.ordner / "KATALOG.md").read_text(encoding="utf-8")
        self.assertLess(text.index("- a:"), text.index("- z:"))

    def test_meldet_unvollstaendigen_kopf(self):
        skill(self.ordner, "gut", "---\nname: gut\ndescription: Vollständig\n---\n")
        skill(self.ordner, "halb", "---\nname: halb\n---\n")
        ausgabe = lauf(self.ordner)
        self.assertIn("Kopf fehlt oder unvollständig", ausgabe)
        self.assertIn("halb", ausgabe)
        text = (self.ordner / "KATALOG.md").read_text(encoding="utf-8")
        self.assertNotIn("halb", text)

    def test_zaehlt_die_geschriebenen_skills(self):
        skill(self.ordner, "a", "---\nname: a\ndescription: A\n---\n")
        skill(self.ordner, "b", "---\nname: b\ndescription: B\n---\n")
        ausgabe = lauf(self.ordner)
        self.assertIn("2 Skills", ausgabe)

    def test_leerer_ordner_schreibt_leeren_katalog(self):
        lauf(self.ordner)
        text = (self.ordner / "KATALOG.md").read_text(encoding="utf-8")
        self.assertEqual(text, "# Skill-Katalog\n\n\n")

    def test_ohne_argument_zeigt_hilfe(self):
        alt = sys.argv
        sys.argv = ["skill_katalog.py"]
        try:
            with self.assertRaises(SystemExit) as fehler:
                with contextlib.redirect_stdout(io.StringIO()):
                    skill_katalog.main()
        finally:
            sys.argv = alt
        self.assertNotEqual(fehler.exception.code, 0)

    def test_beispielskills_ergeben_katalog(self):
        lauf(HIER / "beispiel-skills")
        text = (HIER / "beispiel-skills" / "KATALOG.md").read_text(encoding="utf-8")
        self.assertIn("- brief-schreiben:", text)
        self.assertIn("- tabelle-pruefen:", text)


if __name__ == "__main__":
    unittest.main()
