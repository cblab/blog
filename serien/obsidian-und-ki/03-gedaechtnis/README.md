# Teil 3 – Gedächtnis pflegen

Das Skript `verfall.py` meldet abgelaufene, fehlende, ungültige oder lange zurückliegende Datumsangaben und einen Stand in der Zukunft. Es prüft **keine Inhalte**, versteht keine Widersprüche und ändert nichts.

Alle Befehle aus dem Serienordner ausführen.

Linux:

```bash
python3 03-gedaechtnis/verfall.py beispiele/umzug
python3 03-gedaechtnis/verfall.py beispiele/umzug 90
```

Windows PowerShell:

```powershell
py 03-gedaechtnis\verfall.py beispiele\umzug
py 03-gedaechtnis\verfall.py beispiele\umzug 90
```

Die letzte Zahl ist die gewählte Altersgrenze in Tagen, Standard 180; keine fachlich garantierte Gültigkeitsdauer. `Stand` bezeichnet letzte Inhaltsprüfung. `Gilt bis` ist optional. Format JJJJ-MM-TT. `veraltet` wird übersprungen. Pro Datei wird der erste passende Prüfhinweis ausgegeben; nach Korrektur erneut laufen lassen. Alte Köpfe ohne YAML-Trennlinien bleiben unterstützt.

Die gemeinsame [aktuelle Kündigungsnotiz](../beispiele/umzug/Wissen/Alte%20Wohnung%20Kündigung.md) und der [alte Stand](../beispiele/umzug/Wissen/Kündigung%20alter%20Stand.md) zeigen den Unterschied zwischen „zu prüfen“ und „veraltet“. Auch ein neueres Datum bestätigt die fiktive Kündigungsfrist nicht. Prüfe die Quelle und kennzeichne offene Angaben, bevor du eine Notiz als gültig verwendest.

## Tests

```bash
python3 -m unittest discover -s 03-gedaechtnis/tests -v
```

Unter Windows `py` statt `python3`, Backslashes in Pfaden.

[Zur Serienübersicht](../README.md) · [Voriger Teil](../02-kontext-router/README.md) · [Nächster Teil](../04-skills/README.md)
