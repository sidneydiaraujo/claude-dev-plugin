#!/usr/bin/env python3
"""Teto de linhas por arquivo para o que o ESLint não cobre (C#, Python,
templates HTML/SCSS do Angular, SQL...). Mesmos critérios da regra
quality/max-lines do templates/eslint: testes, arquivos gerados, barrels e
módulos só de tipos/constantes ficam de fora.

Uso (da raiz do projeto):
  python check_max_lines.py                      # mede, falha só com arquivo NOVO acima do teto
  python check_max_lines.py --write-baseline     # grava os infratores atuais como linha de base
  python check_max_lines.py --max 350 --ext .cs .py .html .scss

Linha de base: .max-lines-baseline (um caminho por linha, # para comentário).
Arquivo na linha de base é dívida conhecida: aparece no relatório, não
reprova. Arquivo novo acima do teto reprova (exit 1). A meta é a linha de
base chegar a zero.
"""
import argparse
import os
import re
import sys

DEFAULT_EXT = [".cs", ".py", ".html", ".scss", ".css", ".sql", ".ts", ".tsx", ".js", ".jsx"]

IGNORED_DIRS = {
    "node_modules", "dist", "build", ".next", ".angular", "bin", "obj", "out",
    "generated", "__generated__", "migrations", "migration", "locales",
    "__tests__", "__mocks__", "fixtures", "mocks", "tests", "test",
    ".git", ".venv", "venv", "__pycache__", "coverage", "wwwroot", "docs",
}

# Não é código de produção: testes, configs, stories, gerados por ferramenta.
NON_SOURCE = re.compile(
    r"(\.(test|spec|stories|config|conf)\.[^.]+$)"
    r"|(^test_.*\.py$)|(_test\.py$)"
    r"|(Tests?\.cs$)|(\.g\.cs$)|(\.g\.i\.cs$)|(\.Designer\.cs$)"
    r"|(^AssemblyInfo\.cs$)|(ModelSnapshot\.cs$)"
    r"|(\.d\.ts$)|(\.min\.(js|css)$)"
)
# Barrel ou módulo só de declarações: tamanho não diz nada.
TYPE_BARREL = re.compile(r"^(index|types?|interfaces?|constants?|dtos?|enums?|vo|__init__)\.[^.]+$")


def checkable(rel_path):
    parts = rel_path.split("/")
    for seg in parts[:-1]:
        low = seg.lower()
        if low in IGNORED_DIRS or low.endswith(".tests") or low.endswith(".test"):
            return False
    base = parts[-1]
    return not NON_SOURCE.search(base) and not TYPE_BARREL.match(base)


def count_lines(path):
    with open(path, "rb") as f:
        data = f.read()
    if not data:
        return 0
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def read_baseline(path):
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        return {ln.strip().replace("\\", "/") for ln in f if ln.strip() and not ln.startswith("#")}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--max", type=int, default=350)
    ap.add_argument("--ext", nargs="+", default=DEFAULT_EXT)
    ap.add_argument("--root", default=".")
    ap.add_argument("--baseline", default=".max-lines-baseline")
    ap.add_argument("--write-baseline", action="store_true")
    args = ap.parse_args()

    exts = {e if e.startswith(".") else "." + e for e in args.ext}
    offenders = []
    for dirpath, dirnames, filenames in os.walk(args.root):
        dirnames[:] = [d for d in dirnames if d.lower() not in IGNORED_DIRS]
        for name in filenames:
            if os.path.splitext(name)[1] not in exts:
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, args.root).replace("\\", "/")
            if not checkable(rel):
                continue
            n = count_lines(full)
            if n > args.max:
                offenders.append((n, rel))
    offenders.sort(reverse=True)

    if args.write_baseline:
        with open(args.baseline, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"# Arquivos acima de {args.max} linhas em que ainda não se mexeu.\n")
            f.write("# Remova a linha quando o arquivo for quebrado. Meta: lista vazia.\n")
            for _, rel in offenders:
                f.write(rel + "\n")
        print(f"linha de base gravada: {len(offenders)} arquivo(s) em {args.baseline}")
        return 0

    baseline = read_baseline(args.baseline)
    new = [(n, r) for n, r in offenders if r not in baseline]
    known = [(n, r) for n, r in offenders if r in baseline]
    fixed = sorted(baseline - {r for _, r in offenders})

    print(f"Teto: {args.max} linhas | extensoes: {' '.join(sorted(exts))}")
    print(f"Acima do teto: {len(offenders)} (novos: {len(new)}, na linha de base: {len(known)})")
    for n, r in new:
        print(f"  NOVO  {n:>6}  {r}")
    for n, r in known:
        print(f"  base  {n:>6}  {r}")
    if fixed:
        print(f"Ja cabem no teto, tire da linha de base: {', '.join(fixed)}")
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main())
