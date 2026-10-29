# Obsidian und KI

**Vom Notizbuch zum Assistenten.** Fünf aufeinander aufbauende Anleitungen mit einem gemeinsamen Umzugsbeispiel. Du beginnst mit drei Textdateien und kannst später Notizen gezielt auswählen, ihren Stand prüfen und wiederkehrende Aufgaben mit Skills bearbeiten.

Dieses GitHub-Repository ist die zentrale Quelle für die Beispiele und Anleitungen der Artikelserie auf [christian-blab.com](https://christian-blab.com). Die Blogartikel sind derzeit Entwürfe; ihre öffentlichen Links funktionieren nach der Veröffentlichung. Die Beispiele hier kannst du bereits verwenden.

## Die fünf Teile

| Teil | Anleitung und Material | Artikel |
|---|---|---|
| 1 | [Ein Notizbuch mit Obsidian anlegen](01-obsidian/README.md) | [zxz.nz/obsidian1](https://zxz.nz/obsidian1) |
| 2 | [Passende Notizen auswählen](02-kontext-router/README.md) | [zxz.nz/obsidian2](https://zxz.nz/obsidian2) |
| 3 | [Ein Gedächtnis pflegen](03-gedaechtnis/README.md) | [zxz.nz/obsidian3](https://zxz.nz/obsidian3) |
| 4 | [Skills verwenden](04-skills/README.md) | [zxz.nz/obsidian4](https://zxz.nz/obsidian4) |
| 5 | [Einen Assistenten im Terminal einrichten](05-terminal/README.md) | [zxz.nz/obsidian5](https://zxz.nz/obsidian5) |

Nur bei Bedarf: [WSL unter Windows einrichten](zusatz/wsl/README.md). WSL ist für Obsidian und die Python-Beispiele unter Windows nicht erforderlich.

## Ohne Programmieren anfangen

1. Lade über **Code → Download ZIP** das Repository herunter und entpacke es. Alternativ: [ZIP herunterladen](https://github.com/cblab/blog/archive/refs/heads/main.zip).
2. Öffne in Obsidian den Ordner [`beispiele/umzug`](beispiele/umzug/Start.md) als Vault („Open folder as vault“).
3. Beginne mit `Start.md`. Sie verlinkt die drei Fachnotizen und eine alte Fassung zum Vergleich.
4. Gib einem Chat nur die für deine Frage nötigen Texte. Der Chat kann den lokalen Ordner erst lesen, wenn du Inhalte übergibst oder ein entsprechendes Werkzeug eingerichtet hast.

Alle Angaben sind erfunden. Eine gute erste Frage: **Was ist beim Transport entschieden und was ist noch offen?** Ein Transporter ist vorgesehen, eine Ersparnis wird erwartet. Ein verbindliches Angebot, ein Buchungstermin und Helferzusagen fehlen. Die fiktive Kündigungsfrist ist ausdrücklich zu prüfen.

## Die lokalen Skripte ausprobieren

Python ab 3.10. Router, Datumsprüfung und Skill-Katalog brauchen nur die Standardbibliothek. Den Dokumentimport mit MarkItDown kannst du überspringen.

Öffne das Terminal im **Hauptordner**, der diese README enthält. Ein GitHub-ZIP entpackt sich üblicherweise in `blog-main`. Wenn du Git verwendest:

```bash
git clone https://github.com/cblab/blog.git
cd blog
```

Unter Linux:

```bash
python3 02-kontext-router/router.py beispiele/umzug "Was ist beim Transport entschieden und was ist offen?"
python3 03-gedaechtnis/verfall.py beispiele/umzug
python3 04-skills/skill_katalog.py 04-skills/beispiel-skills
```

Unter Windows in PowerShell:

```powershell
py 02-kontext-router\router.py beispiele\umzug "Was ist beim Transport entschieden und was ist offen?"
py 03-gedaechtnis\verfall.py beispiele\umzug
py 04-skills\skill_katalog.py 04-skills\beispiel-skills
```

Router und Datumsprüfung lesen nur. Der Skill-Katalog schreibt `KATALOG.md` im angegebenen Skills-Ordner. Die drei Skripte rufen kein KI-Modell auf. Wenn du ihre Ausgabe an einen Cloud-Chat übergibst, werden die übergebenen Inhalte an dessen Anbieter gesendet.

## Wie die Materialien zusammenpassen

```text
01-obsidian/         Einstieg und erste Chatübung
02-kontext-router/   Wortsuche und optionaler Dokumentimport
03-gedaechtnis/      Datumsprüfung, Vorlagen, zusätzlicher Garten-Vault
04-skills/           Katalog und zwei Beispielanleitungen
05-terminal/         Optionale OpenCode-1-Leseübung
beispiele/umzug/     Gemeinsamer fiktiver Vault
beispiele/unterlagen/ Eine kleine Quelle für den optionalen Import
zusatz/wsl/          Windows-Zusatz
tools/              Gemeinsame Prüfung
```

Die Notizeigenschaften sind überall gleich: `Titel`, `Thema`, `Status`, `Stand`, `Kurz`, `Quelle`. `Status` verwendet `gilt`, `zu prüfen` oder `veraltet`. `Stand` bezeichnet den Tag der letzten Inhaltsprüfung. Ein optionales `Gilt bis` bezeichnet eine zeitliche Grenze. Datumsformat: `JJJJ-MM-TT`. Die einfachen YAML-Köpfe sind keine automatische Wahrheitsprüfung.

Die Router-Suche vergleicht Wortanfänge. Sie versteht keine Bedeutung und folgt keinen Obsidian-Links. Die Datumsprüfung gibt Pflegehinweise, prüft aber keine Inhalte. Ein Skill beschreibt einen Arbeitsablauf und erteilt keine technischen Rechte. Diese Grenzen gehören zu den Beispielen.

## Alles lokal prüfen

Linux:

```bash
python3 tools/check_series.py
```

Windows:

```powershell
py tools\check_series.py
```

Die Prüfung führt alle Unit-Tests aus, probiert die drei Befehle auf den mitgelieferten Daten aus und kontrolliert die lokalen Markdown-Verweise sowie die Links im gemeinsamen Vault. Sie benötigt keine Anbieterzugänge und installiert nichts. Schreibende Probeläufe verwenden temporäre Ordner. Der optionale Import wird mit einem Ersatz für MarkItDown getestet.

Dieselbe Prüfung ist für GitHub Actions auf Ubuntu und Windows vorbereitet. Ob der jeweilige CI-Lauf bestanden hat, zeigt der Reiter **Actions**. Einen tatsächlichen OpenCode-Modelllauf oder eine WSL-Installation ersetzt diese Prüfung nicht.

## Weiterverwenden

Code und Beispieldaten stehen unter [MIT](LICENSE). Das Graphbild aus dem Artikel hat eine eigene Lizenz und ist nicht Teil dieses Repositorys. Den [Neuaufbau und die geänderten Pfade](CHANGELOG.md) kannst du im Änderungsprotokoll nachlesen.
