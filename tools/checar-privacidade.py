"""Procura dados pessoais em arquivos antes de publicar.

    python tools/checar-privacidade.py            # verifica docs/ e o que está no git
    python tools/checar-privacidade.py caminho/   # verifica uma pasta específica

Sai com código 1 se encontrar algo, então também serve como hook de pre-commit.
Imagens não são lidas: prints precisam de revisão visual (veja docs/README.md).
"""

from __future__ import annotations

import getpass
import re
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".txt", ".py", ".ps1", ".json", ".csv", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".log"}


def build_patterns() -> dict[str, re.Pattern[str]]:
    user = re.escape(getpass.getuser())
    host = re.escape(socket.gethostname())
    patterns = {
        "caminho com usuário": rf"(?i)[a-z]:[\\/]+users[\\/]+{user}\b",
        "nome do usuário": rf"(?i)\b{user}\b",
        "nome do computador": rf"(?i)\b{host}\b",
        "e-mail pessoal": r"(?i)[a-z0-9._%+-]+@(gmail|hotmail|outlook|yahoo|icloud|live)\.[a-z.]+",
        "IP privado": r"\b(10\.\d{1,3}|192\.168|172\.(1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b",
        "endereço MAC": r"\b([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b",
        "token/chave": r"(?i)\b(ghp_|gho_|github_pat_|sk-|hf_)[A-Za-z0-9_]{16,}",
    }
    # O padrão \b (fronteira de palavra) exige a palavra inteira: um usuário público do GitHub como "fulano123" não casa com "fulano".
    return {k: re.compile(v) for k, v in patterns.items()}


SKIP_DIRS = {".git", ".venv", ".privado", "external", "__pycache__", ".pytest_cache", ".ruff_cache"}


def _walk(path: Path) -> list[Path]:
    """Arquivos de uma pasta, pulando o que nunca é publicado (ambiente virtual, material privado...)."""
    if not path.is_dir():
        return [path]
    return [p for p in path.rglob("*") if not SKIP_DIRS.intersection(p.relative_to(path).parts)]


def files_to_check(args: list[str]) -> list[Path]:
    if args:
        return [p for a in args for p in _walk(Path(a))]
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    return sorted({ROOT / f for f in tracked} | set((ROOT / "docs").rglob("*")))


def main() -> int:
    patterns = build_patterns()
    hits = 0
    for path in files_to_check(sys.argv[1:]):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES or path.name == Path(__file__).name:
            continue
        for n, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for label, rx in patterns.items():
                for m in rx.finditer(line):
                    hits += 1
                    rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
                    print(f"[{label}] {rel}:{n}: ...{line[max(0, m.start() - 20): m.end() + 20].strip()}...")
    print(f"\n{hits} ocorrência(s) encontrada(s)." if hits else "Nenhum dado pessoal encontrado.")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
