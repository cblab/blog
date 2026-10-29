# Teil 3 – Gedächtnis pflegen

Das Skript `verfall.py` meldet abgelaufene, fehlende, ungültige oder lange zurückliegende Datumsangaben und einen Stand in der Zukunft. Es prüft **keine Inhalte**, versteht keine Widersprüche und ändert nichts.

Alle Befehle aus dem Hauptordner ausführen.

Linux:

```bash
python3 03-gedaechtnis/verfall.py beispiele/umzug
python3 03-gedaechtnis/verfall.py 03-gedaechtnis/beispiel-garten 90
```

Windows PowerShell:

```powershell
py 03-gedaechtnis\verfall.py beispiele\umzug
py 03-gedaechtnis\verfall.py 03-gedaechtnis\beispiel-garten 90
```

Die letzte Zahl ist die gewählte Altersgrenze in Tagen, Standard 180; keine fachlich garantierte Gültigkeitsdauer. `Stand` bezeichnet letzte Inhaltsprüfung. `Gilt bis` ist optional. Format JJJJ-MM-TT. `veraltet` wird übersprungen. Pro Datei wird der erste passende Prüfhinweis ausgegeben; nach Korrektur erneut laufen lassen. Alte Köpfe ohne YAML-Trennlinien bleiben unterstützt.

`vorlagen/` enthält die bestehenden Startvorlagen (Über mich, Regeln, Entscheidungen). `beispiel-garten/` ist der erhaltene zweite Beispiel-Vault: in Obsidian öffnen, von Tomaten nach Beet 4 und zur veralteten Standortnotiz gehen. Alles sind fiktive Beispieldaten, keine Gartenbauempfehlung. Der Graph stellt Links dar, weder Aktualität noch Wahrheit.

## Tests

```bash
python3 -m unittest discover -s 03-gedaechtnis/tests -v
```

Unter Windows `py` statt `python3`, Backslashes in Pfaden.

[Zur Serienübersicht](../README.md) · [Voriger Teil](../02-kontext-router/README.md) · [Nächster Teil](../04-skills/README.md)
