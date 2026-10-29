# Artikel und Serien auf christian-blab.com

Hier liegen die begleitenden Beispiele, Skripte und Anleitungen zum [Blog von Christian Blab](https://christian-blab.com). Jede Serie bekommt einen eigenen Ordner; unabhängige Artikel können später unter `artikel/<thema>/` dazukommen.

## Serien

| Serie | Inhalt | Einstieg |
|---|---|---|
| Obsidian und KI: Vom Notizbuch zum Assistenten | Fünf Teile mit gemeinsamem Umzugsbeispiel; Notizen, Kontextauswahl, Gedächtnispflege, Skills und Terminal-Assistent. WSL als optionaler Zusatz. | [Zur Serie](serien/obsidian-und-ki/README.md) |

## Beispiele herunterladen

Über **Code → Download ZIP** kannst du das [gesamte Repository herunterladen](https://github.com/cblab/blog/archive/refs/heads/main.zip). Entpacke es und öffne den Ordner der gewünschten Serie. Die jeweilige README erklärt Voraussetzungen und Befehle. Ein ZIP enthält alle Reihen; die Befehle jeder Reihe beginnen in deren eigenem Ordner.

```text
serien/
  obsidian-und-ki/
    README.md
    01-obsidian/
    02-kontext-router/
    03-gedaechtnis/
    04-skills/
    05-terminal/
    beispiele/
    zusatz/
    tools/
```

## Prüfen

Für die bestehende Serie, aus der Repository-Wurzel:

```bash
python3 serien/obsidian-und-ki/tools/check_series.py
```

Unter Windows:

```powershell
py serien\obsidian-und-ki\tools\check_series.py
```

Die Prüfung installiert nichts und benötigt keine Anbieterzugänge. GitHub Actions führt sie auf Windows und Ubuntu aus. Weitere Reihen erhalten eigene Prüfaufrufe.

## Lizenz

Code und Beispieldaten stehen unter [MIT](LICENSE). Abweichend lizenzierte Materialien werden beim jeweiligen Material gekennzeichnet. Die Blogbeiträge sind derzeit Entwürfe; die Beispiele auf GitHub sind bereits verfügbar.
