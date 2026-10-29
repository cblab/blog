# Teil 5: Einen Assistenten im Terminal einrichten

Mit einem Terminal-Assistenten kannst du passende Notizen direkt lesen lassen. Der erste Versuch bleibt eine Leseaufgabe auf einer Kopie der fiktiven Umzugsnotizen. Für Obsidian und den Browserchat aus den vorherigen Teilen ist dieser Schritt optional.

Diese Anleitung und die beiliegende Konfiguration beziehen sich auf **OpenCode 1**. OpenCode 2 verwendet ebenfalls den Befehl `opencode`, hat aber eine eigene Dokumentation. Prüfe vor dem Einrichten mit `opencode --version`, welche Hauptversion du verwendest. Übertrage das Profil nicht ungeprüft auf andere Versionen.

## Eine Testkopie öffnen

1. Kopiere `beispiele/umzug` aus dem Serienordner dieses Repositorys in einen neuen, leeren Testordner außerhalb des Repositorys. Verwende für den ersten Versuch keine echten Dokumente.
2. Kopiere die beiliegende `opencode.json` ebenfalls in diesen Testordner. Überschreibe keine vorhandene Konfiguration.
3. Installiere OpenCode nach der [offiziellen Anleitung](https://opencode.ai/docs/) für dein Betriebssystem, falls es noch nicht installiert ist.
4. Öffne ein Terminal im Testordner und starte `opencode`.
5. Prüfe das gewählte Modell, die Kosten deines Zugangs und die tatsächlich geladenen Berechtigungen, bevor du eine Anfrage sendest. Für einen Anbieterzugang verweist OpenCode auf `/connect`.

Die Testkopie enthält `Start.md`, `Quellen`, `Wissen` und `Entscheidungen` direkt im geöffneten Ordner. Wenn du stattdessen eine weitere Ordnerstufe siehst, wechsle zunächst in den Vault.

## Was das Leseprofil erlaubt

`opencode.json` setzt alle Werkzeuge zunächst auf `deny`. Erlaubt sind ausdrücklich `read`, `glob` und `grep`. Zugriffe außerhalb des Startordners bleiben über `external_directory` gesperrt. Shell-Befehle, Dateiänderungen und das Skill-Werkzeug sind in diesem strikten Profil ebenfalls gesperrt.

Das sind Regeln des Assistenten, **keine Betriebssystem-Sandbox**. Globale oder agentenspezifische Einstellungen, Plugins und andere Softwareversionen können das Verhalten beeinflussen. Prüfe die wirksamen Regeln im verwendeten Client. Ein Startordner allein begrenzt die Betriebssystemrechte eines Prozesses nicht.

Das Profil wurde syntaktisch und gegen die offizielle Beschreibung geprüft. Die lokale Serienprüfung führt keinen OpenCode-Modelllauf aus und bestätigt daher nicht die Durchsetzung in deiner konkreten Installation.

## Der erste Auftrag

```text
Lies Start.md und die für die Transportplanung relevanten Notizen.
Nenne die relative Datei und Belegstelle für jede Angabe.
Was ist entschieden, was ist nur erwartet und was ist noch offen?
Behandle „zu prüfen“ nicht als bestätigte Tatsache.
Ändere keine Dateien und führe keine Shell-Befehle aus.
Wenn du eine Datei nicht lesen darfst, melde die Grenze.
```

Ein Transporter ist vorgesehen. Eine Ersparnis wird erwartet; ein verbindliches Angebot, Termin und Helferzusagen fehlen. Prüfe die Belege und anschließend, ob die Testdateien unverändert geblieben sind. Verlangt der Assistent Schreibrechte, kläre den Grund, statt sie pauschal zu erteilen.

Wenn du ein Cloud-Modell verwendest, kann der Assistent die gelesenen Notizen an dessen Anbieter senden. Ein lokal gestartetes Programm bedeutet nicht automatisch eine vollständig lokale Verarbeitung.

## Skills erst danach ergänzen

Die Anleitung `brief-schreiben` aus [Teil 4](../04-skills/README.md) kannst du für einen ersten Versuch manuell als Inhalt übergeben. Automatische Skill-Erkennung benötigt den [dokumentierten Ablageort](https://opencode.ai/docs/skills/) und das Skill-Werkzeug. Dieses Werkzeug ist im strikten Leseprofil gesperrt; es wird nicht allein durch das Kopieren einer Anleitung freigeschaltet.

Erweitere die Regeln nur bewusst für einen konkreten Test. Ein Skill enthält eine Arbeitsanweisung, keine zusätzlichen Zugriffsrechte und keine Bestätigung der verwendeten Fakten.

## MCP und tmux sind Ergänzungen

Für die vorhandenen Dateilesewerkzeuge ist kein zusätzlicher MCP-Server nötig. Ergänze einen Dienst erst, wenn du ein konkretes weiteres Werkzeug brauchst. Prüfe dessen Herkunft, Zugriffe und Datenübertragungen anhand der [MCP-Dokumentation von OpenCode](https://opencode.ai/docs/mcp-servers/).

Unter Linux oder WSL kann tmux eine Terminalsitzung vom sichtbaren Fenster lösen. Wenn tmux bereits installiert ist:

```bash
tmux new -s obsidian-test
```

Starte darin einen lokalen Test ohne Modellzugang:

```bash
for i in $(seq 1 30); do echo "Sekunde $i"; sleep 1; done
```

Mit `Strg+b`, dann `d` löst du dich aus der Sitzung. Zurück kommst du mit:

```bash
tmux attach -t obsidian-test
```

tmux pausiert die Aufgabe nicht, repariert keine fehlerhafte Modellanfrage und übersteht keinen Rechnerneustart. Wenn der Test fertig ist, schließt `exit` die Testsitzung.

## Weitere Quellen

- [Berechtigungen in OpenCode 1](https://opencode.ai/docs/permissions/)
- [Optionale WSL-Anleitung](../zusatz/wsl/README.md)

[Zur Serienübersicht](../README.md) · [Voriger Teil](../04-skills/README.md)
