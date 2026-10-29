#!/usr/bin/env python3
"""Prüft die Serienbeispiele lokal, ohne Anbieteranfragen oder Installationen."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
PARTS = ('01-obsidian', '02-kontext-router', '03-gedaechtnis', '04-skills', '05-terminal')


def run(*args: str) -> str:
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    result = subprocess.run([sys.executable, '-X', 'utf8', *args], cwd=ROOT,
                            capture_output=True, text=True, encoding='utf-8', env=env)
    if result.returncode:
        raise RuntimeError(f"Fehler bei {' '.join(args)}\n{result.stdout}{result.stderr}")
    print(f"OK: {' '.join(args)}")
    if '-m' in args:
        print(result.stderr.strip())
    return result.stdout


def check_links() -> int:
    checked = 0
    for path in [REPO_ROOT / 'README.md', *ROOT.rglob('*.md')]:
        if '.git' in path.relative_to(REPO_ROOT).parts:
            continue
        text = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
        for raw in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)', text):
            url = urlsplit(raw)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (path.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(REPO_ROOT) or not target.exists():
                raise RuntimeError(f'Lokaler Link fehlt: {path.relative_to(REPO_ROOT)} -> {raw}')
            checked += 1
    vault = ROOT / 'beispiele/umzug'
    notes = list(vault.rglob('*.md'))
    titles = {path.stem for path in notes}
    for path in notes:
        text = path.read_text(encoding='utf-8')
        for title in re.findall(r'\[\[([^\]|#]+)', text):
            if title not in titles:
                raise RuntimeError(f'Notizlink fehlt: {path.name} -> {title}')
            checked += 1
    print(f'OK: {checked} lokale Dokument- und Vault-Verweise')
    return checked


def check_examples() -> None:
    output = run('02-kontext-router/router.py', 'beispiele/umzug',
                 'Was ist beim Transport entschieden und was ist offen?')
    # Relative paths use / on every supported platform.
    if '--- Notiz: Entscheidungen/Transport planen.md' not in output:
        raise RuntimeError('Die Transportentscheidung wurde nicht ausgewählt.')
    if '--- Notiz: Wissen/Kündigung alter Stand.md' in output:
        raise RuntimeError('Der alte Stand wurde als aktueller Kandidat ausgewählt.')
    for term in ('unbestätigt', 'nicht belegt'):
        if term not in output:
            raise RuntimeError('Die Hinweise auf ungeprüfte oder fehlende Angaben fehlen.')
    run('03-gedaechtnis/verfall.py', 'beispiele/umzug')
    with tempfile.TemporaryDirectory() as tmp:
        skills = Path(tmp) / 'skills'
        shutil.copytree(ROOT / '04-skills/beispiel-skills', skills,
                        ignore=shutil.ignore_patterns('KATALOG.md'))
        run('04-skills/skill_katalog.py', str(skills))
        catalog = (skills / 'KATALOG.md').read_text(encoding='utf-8')
        entries = [line for line in catalog.splitlines() if line.startswith('- ')]
        if len(entries) != 2 or not all(name in catalog for name in ('brief-schreiben', 'tabelle-pruefen')):
            raise RuntimeError('Der Beispielkatalog enthält nicht die beiden erwarteten Skills.')
    profile = json.loads((ROOT / '05-terminal/opencode.json').read_text(encoding='utf-8'))
    if profile.get('permission', {}).get('*') != 'deny':
        raise RuntimeError('Das Leseprofil muss standardmäßig Werkzeuge sperren.')
    print('OK: Leseprofil syntaktisch geprüft; kein Modelllauf ausgeführt')


def main() -> int:
    try:
        if sys.version_info < (3, 10):
            raise RuntimeError('Python ab Version 3.10 erforderlich.')
        for part in PARTS:
            if not (ROOT / part / 'README.md').is_file():
                raise RuntimeError(f'Die Anleitung zu {part} fehlt.')
        for part in ('02-kontext-router', '03-gedaechtnis', '04-skills'):
            run('-m', 'unittest', 'discover', '-s', f'{part}/tests', '-v')
        check_links()
        check_examples()
    except (RuntimeError, OSError, ValueError) as exc:
        print(f'FEHLER: {exc}', file=sys.stderr)
        return 1
    print('OK: Serienbeispiele, Unit-Tests und lokale Verweise geprüft. Keine Anbieteranfragen.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
