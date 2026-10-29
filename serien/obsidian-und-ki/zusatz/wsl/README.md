# Zusatz: WSL unter Windows

WSL ist optional. Obsidian und die Python-Skripte funktionieren auch ohne WSL unter Windows. Verwende WSL, wenn du mit Linux-Werkzeugen wie tmux arbeiten möchtest.

Der [WSL-Blogartikel](https://zxz.nz/wsl) gehört als Zusatz zur Serie. Die [Microsoft-Anleitung](https://learn.microsoft.com/en-us/windows/wsl/install) beschreibt Voraussetzungen und aktuelle Installationswege.

Für den einfachen Installationsweg nennt Microsoft Windows 10 ab Version 2004, Build 19041, oder Windows 11. In einer PowerShell als Administrator:

```powershell
wsl --install -d Ubuntu
```

Folge den Meldungen und starte bei Bedarf neu. Öffne Ubuntu und lege den Linux-Benutzer an. Prüfe anschließend in **PowerShell**:

```powershell
wsl --list --verbose
```

In **Ubuntu** verwendest du Linux-Befehle:

```bash
pwd
python3 --version
```

Die Beispiele benötigen Python ab 3.10. Im Serienordner der entpackten Repository-Kopie:

```bash
python3 02-kontext-router/router.py beispiele/umzug "Was ist beim Transport entschieden und was ist offen?"
```

`py` gehört in diesen Anleitungen zu Windows, `python3` zur Linux-Umgebung. Windows-Dateien unter `C:\Users\...` erreichst du in WSL üblicherweise über `/mnt/c/Users/...`. Beginne mit einer Kopie der fiktiven Beispieldaten. `wsl --shutdown` beendet alle WSL-Prozesse; sichere Arbeit vor einem bewussten Neustart.

Zurück zur [Serienübersicht](../../README.md) oder zu [Teil 5](../../05-terminal/README.md).
