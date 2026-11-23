#!/usr/bin/env python3
"""
Check that every palette (palettes.json and each sample's Baraat / Walima palette) stays readable.

    python studio/tools/palette_check.py            report problems
    python studio/tools/palette_check.py --all      also print every palette's numbers

Rules (WCAG contrast ratios): names/text on card >= 7, highlight text on card >= 4.5, intro text on the scene
background >= 4.5, gold lines visible on card >= 1.8 and on background >= 1.6, envelope/paper on background >= 1.3.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = [("ink", "cd", 7.0, "names/text on card"), ("ink2", "cd", 4.5, "highlight text on card"),
         ("it", "bg", 4.5, "intro text on background"), ("acc", "cd", 1.8, "gold lines on card"),
         ("acc", "bg", 1.6, "gold lines on background"), ("ef", "bg", 1.3, "paper/envelope on background")]


def lum(hexc):
    h = hexc.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def check(name, p, show):
    bad = []
    nums = []
    for fg, bg, need, what in RULES:
        if fg not in p or bg not in p:
            bad.append(f"missing {fg}/{bg}")
            continue
        c = contrast(p[fg], p[bg])
        nums.append(f"{fg}/{bg} {c:.1f}")
        if c < need:
            bad.append(f"{what}: {fg} {p[fg]} on {bg} {p[bg]} = {c:.2f} (needs {need})")
    if show:
        print(f"{name}: " + ", ".join(nums))
    for b in bad:
        print(f"  PROBLEM {name}: {b}")
    return len(bad)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    problems = 0
    pals = json.loads((ROOT / "palettes.json").read_text(encoding="utf-8-sig"))
    for k, p in pals.items():
        problems += check(f"palettes.json:{k}", p, a.all)
    samples = json.loads((ROOT / "samples.json").read_text(encoding="utf-8-sig"))
    for i, s in enumerate(samples, 1):
        for ev in ("baraat", "walima"):
            p = (s.get("pal") or {}).get(ev)
            if p:
                problems += check(f"sample {i} {s.get('name')} [{ev}]", p, a.all)
    print(f"{problems} problem(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
