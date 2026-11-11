#!/usr/bin/env python3
"""Static scan of a Lean 4 source tree for admitted proofs.

Strips line comments, nested block comments and string literals, then counts `sorry`,
`admit`, `native_decide`, `axiom` declarations, and theorem/lemma declarations.
This is a text scan, not a build: it cannot see what `lake build` would report.

Usage:
    git archive upstream/main Lean | tar -x -C /some/empty/dir
    python3 oph_lean_scan.py /some/empty/dir/Lean
"""
import pathlib
import re
import sys
from collections import Counter


def strip(src):
    out, i, depth, in_str, n = [], 0, 0, False, len(src)
    while i < n:
        if depth == 0 and not in_str and src.startswith("--", i):
            j = src.find("\n", i)
            i = n if j < 0 else j
            continue
        if not in_str and src.startswith("/-", i):
            depth += 1
            i += 2
            continue
        if depth > 0 and src.startswith("-/", i):
            depth -= 1
            i += 2
            continue
        if depth > 0:
            if src[i] == "\n":
                out.append("\n")
            i += 1
            continue
        c = src[i]
        if c == '"' and (i == 0 or src[i - 1] != "\\"):
            in_str = not in_str
            out.append(" ")
            i += 1
            continue
        out.append(" " if in_str and c != "\n" else c)
        i += 1
    return "".join(out)


MODS = r"(?:@\[[^\]]*\]\s*)*(?:private\s+|protected\s+|noncomputable\s+)*"
PATTERNS = {
    "sorry": r"\bsorry\b",
    "admit": r"\badmit\b",
    "native_decide": r"\bnative_decide\b",
    "axiom": r"^\s*" + MODS + r"axiom\s",
    "theorem": r"^\s*" + MODS + r"theorem\s",
    "lemma": r"^\s*" + MODS + r"lemma\s",
}


def main(root):
    totals = Counter()
    flagged = Counter()
    for path in sorted(pathlib.Path(root).rglob("*.lean")):
        if ".lake" in path.parts:
            continue
        text = strip(path.read_text(errors="replace"))
        totals["files"] += 1
        for name, pattern in PATTERNS.items():
            hits = len(re.findall(pattern, text, re.M))
            totals[name] += hits
            if hits and name in ("sorry", "admit", "native_decide", "axiom"):
                flagged[(name, str(path.relative_to(root)))] += hits
    print(dict(totals))
    for (name, rel), hits in sorted(flagged.items()):
        print(f"  {name}: {rel} ({hits})")


if __name__ == "__main__":
    main(sys.argv[1])
